import queue
import threading
import time
from pathlib import Path
from datetime import datetime

import forex_trading


class SlidingWindow:
    def __init__(self, length) -> None:
        self.data = [0] * length

    def add(self, element):
        self.data.append(element)
        self.data.pop(0)


PACKAGE_ROOT = Path(forex_trading.__file__).resolve().parent
DATAPATH = PACKAGE_ROOT / "datasets"
file_name = DATAPATH / "LMAX EUR_USD 1 Minute.txt"
f = open(file_name)
f.readline()

close = SlidingWindow(5)
high = SlidingWindow(5)
low = SlidingWindow(5)
sw = SlidingWindow(5)

datastream = queue.Queue()


def get_tick():
    tick = {}
    values = f.readline().rstrip("\n").split(",")
    timestamp_string = values[0] + " " + values[1]
    ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S.%f")
    tick[ts] = float(values[2])
    return tick


def get_sample(f):
    sample = {}
    values = f.readline().rstrip("\n").split(",")
    timestamp_string = "0" + values[0] + " " + values[1]
    ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S")
    sample["open"] = float(values[2])
    sample["high"] = float(values[3])
    sample["low"] = float(values[4])
    sample["close"] = float(values[5])
    sample["UpVolume"] = int(values[6])
    sample["DownVolume"] = int(values[7])
    sample["Datetime"] = ts
    return sample


def emulate_bar_stream():
    while True:
        time.sleep(1)
        datastream.put(get_sample(f))


def retrieve_bars():
    while True:
        data_point = datastream.get()
        sw.add(data_point)
        print(sw.data)


data_source_thread = threading.Thread(target=emulate_bar_stream)
data_receiver_thread = threading.Thread(target=retrieve_bars)
data_source_thread.start()
data_receiver_thread.start()
