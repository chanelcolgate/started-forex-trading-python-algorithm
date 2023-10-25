from time import sleep

from forex_trading.common.DeviceDataManager import DeviceDataManager


def devicedatamanager():
    dataMgr = DeviceDataManager()
    dataMgr.startManager()
    sleep(65)
    dataMgr.stopManager()
