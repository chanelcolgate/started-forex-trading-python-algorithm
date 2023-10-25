import logging

from forex_trading.common.IDataMessageListener import IDataMessageListener
from forex_trading.system.SystemPerformanceManager import (
    SystemPerformanceManager,
)
from forex_trading.data.SystemPerformanceData import SystemPerformanceData


class DeviceDataManager(IDataMessageListener):
    def __init__(self) -> None:
        self.sysPerfMgr = SystemPerformanceManager()
        self.sysPerfMgr.setDataMessageListener(listener=self)
        logging.info("Local system perforamnce tracking enabled")

    def startManager(self) -> None:
        logging.info("Starting DeviceDataManager...")

        if self.sysPerfMgr:
            self.sysPerfMgr.startManager()

        logging.info("Started DeviceManager.")

    def stopManager(self) -> None:
        logging.info("Stopping DeviceDataManager...")

        if self.sysPerfMgr:
            self.sysPerfMgr.stopManager()

        logging.info("Stopped DeviceDataManager.")

    def handleSystemPerformanceMessage(
        self, data: SystemPerformanceData
    ) -> bool:
        if data:
            logging.debug(
                f"Incoming system performance message received (from sys perf manager): {str(data)}"
            )
            return True
        else:
            logging.warning(
                "Incoming system performance data is invalid (null). Ignoring."
            )
            return False
