from forex_trading.data.BaseIotData import BaseIotData
from forex_trading.common import ConfigConst


class SystemPerformanceData(BaseIotData):
    def __init__(self, d=None) -> None:
        super().__init__(
            name=ConfigConst.SYSTEM_PERF_NAME,
            typeID=ConfigConst.SYSTEM_PERF_TYPE,
            d=d,
        )
        self.cpuUtil = ConfigConst.DEFAULT_VAL
        self.memUtil = ConfigConst.DEFAULT_VAL
        self.diskUtil = ConfigConst.DEFAULT_VAL

    def setCpuUtilization(self, cpuUtil):
        self.cpuUtil = cpuUtil
        self.updateTimeStamp()

    def setDiskUtilization(self, diskUtil):
        self.diskUtil = diskUtil
        self.updateTimeStamp()

    def setMemoryUtilization(self, memUtil):
        self.memUtil = memUtil
        self.updateTimeStamp()

    def __str__(self):
        return f"cpuUtil={self.cpuUtil}, memUtil={self.memUtil}, diskUtil={self.diskUtil}"
