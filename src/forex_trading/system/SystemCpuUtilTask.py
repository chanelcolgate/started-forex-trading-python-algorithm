import psutil

from forex_trading.common import ConfigConst
from forex_trading.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemCpuUtilTask(BaseSystemUtilTask):
    def __init__(self) -> None:
        super().__init__(
            name=ConfigConst.CPU_UTIL_NAME, typeID=ConfigConst.CPU_UTIL_NAME
        )

    def getTelemetryValue(self) -> float:
        return psutil.cpu_percent()
