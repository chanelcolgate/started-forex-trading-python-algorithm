import time
import threading
import queue
from datetime import datetime
from pathlib import Path

import forex_trading
from forex_trading.datasets.csv_tick_reader import CSVTickReader

PACKAGE_ROOT = Path(forex_trading.__file__).resolve().parent
DATAPATH = PACKAGE_ROOT / "datasets"
tickRdr = CSVTickReader(source=DATAPATH / "EURUSD_1_TICK.csv").data_iter()
next(tickRdr)

datastream = queue.Queue()
bars = {}


def emulate_tick_stream():
    while True:
        time.sleep(1)
        temp = next(tickRdr)
        datastream.put(temp)


def trading_algo():
    while True:
        temp = datastream.get()
        print("Received tick ", temp)


def compressor():
    bar = {}
    while True:
        tick = datastream.get()
        current_time = datetime.now()
        if current_time.second == 0:
            bars[current_time] = dict(bar)
            bar["open"] = list(tick.values())[0]
            bar["high"] = list(tick.values())[0]
            bar["low"] = list(tick.values())[0]
            print(bars)
        else:
            try:
                bar["high"] = max([bar["high"], list(tick.values())[0]])
                bar["low"] = min([bar["low"], list(tick.values())[0]])
                bar["close"] = list(tick.values())[0]
            except:
                print(str(current_time), " bar forming...")


data_source_thread = threading.Thread(target=emulate_tick_stream)
data_receiver_thread = threading.Thread(target=trading_algo)
data_source_thread.start()
data_receiver_thread.start()
