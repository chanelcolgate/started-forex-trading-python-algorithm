import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

from forex_trading.datasets.txt_tick_reader import TxtTickReader, DATAPATH
from demo import demo, tabs, gr

with demo:
    with tabs:
        with gr.TabItem("Simple plots of market data") as item:
            tickRdr = TxtTickReader(
                source=DATAPATH / "LMAX EUR_USD 1 Minute.txt"
            )
            open = []
            high = []
            low = []
            close = []
            ts = []
            for i, bar in enumerate(tickRdr.data_iter()):
                if i > 200:
                    break
                if i > 100:
                    open.append(bar["open"])
                    high.append(bar["high"])
                    low.append(bar["low"])
                    close.append(bar["close"])
                    ts.append(bar["Datetime"])
                    data = pd.DataFrame(
                        {
                            "open": open,
                            "high": high,
                            "low": low,
                            "close": close,
                            "ts": ts,
                        }
                    )

            base = alt.Chart(data).encode(
                alt.X("ts:T", axis=alt.Axis(labelAngle=-45)),
                color=alt.condition(
                    "datum.open <= datum.close",
                    alt.value("#06982d"),
                    alt.value("#ae1325"),
                ),
            )
            chart = alt.layer(
                base.mark_rule().encode(
                    alt.Y("low:Q", title="Price", scale=alt.Scale(zero=False)),
                    alt.Y2("high:Q"),
                ),
                base.mark_bar().encode(alt.Y("open:Q"), alt.Y2("close:Q")),
            ).interactive()
            gr.Plot(value=chart)
