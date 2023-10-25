from __future__ import annotations
import logging
import time
import json
from queue import Queue
from pathlib import Path
from datetime import datetime

import apscheduler
import pandas as pd
from websocket import create_connection
from apscheduler.schedulers.background import BackgroundScheduler

import forex_trading
from forex_trading.datasets.txt_tick_reader import TxtTickReader, DATAPATH
from forex_trading.common.IDataMessageListener import IDataMessageListener


def moving_average(data):
    return sum(data) / len(data)


def stochastic(high, low, close):
    max_price = max(high)
    min_price = min(low)
    return (close[-1] - min_price) / (max_price - min_price)


class SlidingWindow:
    def __init__(self, length) -> None:
        self.data = [0] * length

    def add(self, element):
        self.data.append(element)
        self.data.pop(0)


class FixSourceManager:
    def __init__(self, use_emulator: bool = True) -> None:
        self.pollRate = 1
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.handleTelemetry, "interval", seconds=self.pollRate
        )
        url = "wss://public-data-api.london-demo.lmax.com/v1/web-socket"
        subscription_msg = '{"type": "SUBSCRIBE","channels": [{"name": "ORDER_BOOK","instruments": ["eur-usd"]}]}'

        self.use_emulator = use_emulator
        if not use_emulator:
            self.ws = create_connection(url)
            self.ws.send(subscription_msg)
        else:
            self.tickRdr = TxtTickReader(
                source=DATAPATH / "LMAX EUR_USD 1 Minute.txt"
            ).data_iter()
            next(self.tickRdr)

        self.query_queue = Queue()
        self.dataMsgListener = None

    def setDataMessageListener(self, listener: "IDataMessageListener") -> None:
        if listener:
            self.dataMsgListener = listener

    def handleTelemetry(self) -> None:
        try:
            if not self.use_emulator:
                tickData = json.loads(self.ws.recv())
            else:
                tickData = next(self.tickRdr)
            self.query_queue.put(tickData)

            if self.dataMsgListener:
                self.dataMsgListener.setQueryQueue(query_queue=self.query_queue)
        except Exception:
            self.stopManager()

    def startManager(self) -> bool:
        logging.info("Started FixSourceManager.")

        if not self.scheduler.running:
            self.scheduler.start()
            return True
        else:
            logging.warning("FixSourceManager scheduler already started.")
            return False

    def stopManager(self) -> bool:
        logging.info("Stopped FixSourceManager.")

        try:
            self.query_queue.put(None)
            self.scheduler.shutdown()
            return True
        except Exception:
            logging.warning("FixSourceManager scheduler already stopped")
            return False


class FixReceivedManager:
    def __init__(self) -> None:
        self.pollRate = 1
        self.scheduler = BackgroundScheduler(
            {"apscheduler.job_defaults.max_instances": 12}
        )
        self.scheduler.add_job(
            self.handleTelemetry, "interval", seconds=self.pollRate
        )
        self.dataMsgListener = None

    def setDataMessageListener(self, listener: "IDataMessageListener") -> None:
        if listener:
            self.dataMsgListener = listener

    def handleTelemetry(self) -> None:
        if self.dataMsgListener:
            tickData = self.dataMsgListener.getQueryQueue()
            if tickData is None:
                self.stopManager()
            self.dataMsgListener.handleFixReceivedMessage(tickData)

    def startManager(self):
        logging.info("Started FixReceivedManager")
        if not self.scheduler.running:
            self.scheduler.start()
            return True
        else:
            logging.warning(
                "FixReceivedManager scheduler already started. Ignoring."
            )
            return False

    def stopManager(self):
        logging.info("Stopped FixReceivedManager")
        try:
            self.scheduler.shutdown()
            return True
        except Exception:
            logging.warning(
                "FixReceivedManager schduler already stopped. Ignoring"
            )
            return False


class FixDataManager(IDataMessageListener):
    def __init__(self) -> None:
        self.use_emulator = False
        self.make_bar = True
        self.fixSourceMgr = FixSourceManager(self.use_emulator)
        self.fixRecMgr = FixReceivedManager()

        self.fixSourceMgr.setDataMessageListener(listener=self)
        self.fixRecMgr.setDataMessageListener(listener=self)

        self.query_queue = None
        logging.info("Local fix adapter manager simulating enabled")

        window_size = 30

        if not self.use_emulator:
            self.bids = SlidingWindow(window_size)
            self.asks = SlidingWindow(window_size)
        elif not self.use_emulator and self.make_bar:
            self.open = 0
            self.close = 0
            self.high = 0
            self.low = 0
        else:
            self.sw = SlidingWindow(window_size)
            self.close = SlidingWindow(window_size)
            self.high = SlidingWindow(window_size)
            self.low = SlidingWindow(window_size)

        # make bar
        self.bars = pd.DataFrame(
            columns=["Timestamp", "Open", "High", "Low", "Close"]
        )
        self.resolution = 10
        self.last_sample_ts = 0

    def startManager(self) -> None:
        logging.info("Starting FixDataManager...")

        if self.fixSourceMgr:
            self.fixSourceMgr.startManager()

        if self.fixRecMgr:
            self.fixRecMgr.startManager()

        logging.info("Started FixDataManager.")

    def stopManager(self) -> None:
        logging.info("Stopping FixDataManager...")

        self.fixSourceMgr.stopManager()
        self.fixRecMgr.stopManager()

        logging.info("Stopped FixDataManager.")

    def setQueryQueue(self, query_queue):
        if query_queue:
            self.query_queue = query_queue

    def getQueryQueue(self):
        return self.query_queue.get()

    def handleFixReceivedMessage(self, tickData):
        if (
            not self.use_emulator
            and "bids" in tickData.keys()
            and not self.make_bar
        ):
            bid = float(tickData["bids"][0]["price"])
            ask = float(tickData["asks"][0]["price"])
            self.bids.add(bid)
            self.asks.add(ask)
            logging.debug(f"{bid}, {ask}")
        elif (
            not self.use_emulator
            and "bids" in tickData.keys()
            and self.make_bar
        ):
            ts = datetime.strptime(
                tickData["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            last_bid = float(tickData["bids"][0]["price"])

            if self.last_sample_ts == 0:
                self.last_sample_ts = ts
                self.open = self.high = self.low = self.close = last_bid

            delta = ts - self.last_sample_ts
            # print(f"Received tick: {tickData}")

            if delta.seconds >= self.resolution:
                bar = pd.DataFrame(
                    [[self.open, self.high, self.low, self.close, ts]],
                    columns=["Open", "High", "Low", "Close", "Timestamp"],
                )
                self.bars = pd.concat([self.bars, bar])
                self.last_sample_ts = ts
                self.open = self.high = self.low = self.close = last_bid

                if len(self.bars) > 300:
                    self.bars = self.bars.iloc[1:, :]
            else:
                self.high = max([self.high, last_bid])
                self.low = min([self.low, last_bid])
                self.close = last_bid
        elif "close" in tickData.keys():
            self.close.add(tickData["close"])
            self.high.add(tickData["high"])
            self.low.add(tickData["low"])
            ma = moving_average(self.close.data)
            stoch = stochastic(self.high.data, self.low.data, self.close.data)
            logging.debug(f"Bar retrived {self.close.data[-1]}, {ma}, {stoch}")


if __name__ == "__main__":
    fixDataMgr = FixDataManager()
    fixDataMgr.startManager()
    time.sleep(1)
    while True:
        if fixDataMgr.getQueryQueue() is None:
            fixDataMgr.stopManager()
            break
