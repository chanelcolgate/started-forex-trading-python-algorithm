import logging

from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler

from forex_trading.system.SystemCpuUtilTask import SystemCpuUtilTask
from forex_trading.system.SystemDiskUtilTask import SystemDiskUtilTask
from forex_trading.system.SystemMemUtilTask import SystemMemUtilTask
from forex_trading.common import ConfigConst
from forex_trading.common.IDataMessageListener import IDataMessageListener
from forex_trading.data.SystemPerformanceData import SystemPerformanceData


class SystemPerformanceManager:
    def __init__(self):
        self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        self.locationID = ConfigConst.NOT_SET

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, "interval", seconds=5)

        self.cpuUtilTask = SystemCpuUtilTask()
        self.diskUtilTask = SystemDiskUtilTask()
        self.memUtilTask = SystemMemUtilTask()

        self.dataMsgListner = None

    def setDataMessageListener(self, listener: "IDataMessageListener") -> None:
        if listener:
            self.dataMsgListner = listener

    def handleTelemetry(self) -> None:
        self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        self.diskUtilPct = self.diskUtilTask.getTelemetryValue()
        self.memUtilPct = self.memUtilTask.getTelemetryValue()

        logging.debug(
            f"CPU utilization is {self.cpuUtilPct} percent, disk utilization is {self.diskUtilPct} percent and memory utilization is {self.memUtilPct} percent"
        )

        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(self.cpuUtilPct)
        sysPerfData.setMemoryUtilization(self.memUtilPct)
        sysPerfData.setDiskUtilization(self.diskUtilPct)

        if self.dataMsgListner:
            self.dataMsgListner.handleSystemPerformanceMessage(sysPerfData)

    def startManager(self):
        logging.info("Started SystemPerformanceManager.")
        if not self.scheduler.running:
            self.scheduler.start()
        else:
            logging.warning(
                "SystemPerformanceManager scheduler already started. Ignoring."
            )

    def stopManager(self):
        logging.info("Stopped SystemPerformanceManager.")
        try:
            self.scheduler.shutdown()
        except Exception:
            logging.warning(
                "SystemPerformanceManager scheduler already stopped. Ignoring."
            )
