import time
import pandas as pd
import altair as alt
from multiprocessing import Process, Queue

from demo import demo, tabs, gr
from forex_trading.fin_info_exchange.FixAdapterManager import FixDataManager

results_queue = Queue()


def put_data():
    buy_signals_x = []
    buy_signals_y = []
    sell_signals_x = []
    sell_signals_y = []
    window_size = 30
    fixDataMgr = FixDataManager()
    fixDataMgr.startManager()
    time.sleep(1)
    while True:
        if fixDataMgr.getQueryQueue() is None:
            fixDataMgr.stopManager()
            break

        for i in range(1, window_size):
            if fixDataMgr.bids.data[i] > fixDataMgr.asks.data[i - 1]:
                buy_signals_x.append(i)
                buy_signals_y.append(fixDataMgr.bids.data[i] - 0.0001)
            if fixDataMgr.asks.data[i] < fixDataMgr.bids.data[i - 1]:
                sell_signals_x.append(i)
                sell_signals_y.append(fixDataMgr.asks.data[i] + 0.0001)

        results_queue.put(
            dict(
                signals_x=buy_signals_x,
            )
        )


def get_data():
    data = results_queue.get()
    return pd.DataFrame(data)


proc = Process(target=put_data)
proc.start()

with demo:
    with tabs:
        with gr.TabItem("Live Tick Chart") as item:
            df = gr.DataFrame(get_data, every=1)
