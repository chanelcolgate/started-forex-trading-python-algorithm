import psutil

from forex_trading.common import ConfigConst
from forex_trading.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemDiskUtilTask(BaseSystemUtilTask):
    def __init__(self) -> None:
        super().__init__(
            name=ConfigConst.DISK_UTIL_NAME, typeID=ConfigConst.DISK_UTIL_TYPE
        )

    def getTelemetryValue(self) -> float:
        return psutil.disk_usage("/").percent
