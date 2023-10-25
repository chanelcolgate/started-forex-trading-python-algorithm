import time
import threading
import logging

from forex_trading.fin_info_exchange.FixAdapterManager import FixDataManager
from multiprocessing import Process, Queue

results_queue = Queue()


def fixdatamanager():
    fixDataMgr = FixDataManager()
    fixDataMgr.startManager()
    time.sleep(1)
    while True:
        if fixDataMgr.getQueryQueue() is None:
            fixDataMgr.stopManager()
            break
        results_queue.put(fixDataMgr.getQueryQueue())


def test_fixdatamanager():
    proc = Process(target=fixdatamanager)
    proc.start()
    time.sleep(60)
    logging.debug(f"zzzzz{results_queue.get()}zzzzz")
    proc.join()
