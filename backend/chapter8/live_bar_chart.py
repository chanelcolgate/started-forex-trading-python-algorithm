import time

import pandas as pd
import altair as alt
from multiprocessing import Process, Queue

from demo import demo, tabs, gr
from forex_trading.fin_info_exchange.FixAdapterManager import FixDataManager

results_queue = Queue()


def put_data():
    fixDataMgr = FixDataManager()
    fixDataMgr.startManager()
    time.sleep(1)
    while True:
        if fixDataMgr.getQueryQueue() is None:
            fixDataMgr.stopManager()
            break

        results_queue.put(fixDataMgr.bars)


def get_data():
    data = results_queue.get()
    return pd.DataFrame(data)


def make_bar():
    data = results_queue.get()
    df = pd.DataFrame(data)

    base = alt.Chart(df).encode(
        alt.X("Timestamp:T", axis=alt.Axis(labelAngle=-45)),
        color=alt.condition(
            "datum.Open <= datum.Close",
            alt.value("#06982d"),
            alt.value("#ae1325"),
        ),
    )

    chart = alt.layer(
        base.mark_rule().encode(
            alt.Y("Low:Q", title="Price", scale=alt.Scale(zero=False)),
            alt.Y2("High:Q"),
        ),
        base.mark_bar().encode(alt.Y("Open:Q"), alt.Y2("Close:Q")),
    ).interactive()
    return chart


proc = Process(target=put_data)
proc.start()

with demo:
    with tabs:
        with gr.TabItem("Live Bar Chart") as item:
            # df = gr.DataFrame(get_data, every=5)
            # print(df.value)
            gr.Plot(value=make_bar, every=10)
