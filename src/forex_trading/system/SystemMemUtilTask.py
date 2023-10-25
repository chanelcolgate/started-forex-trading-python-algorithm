import psutil

from forex_trading.common import ConfigConst
from forex_trading.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemMemUtilTask(BaseSystemUtilTask):
    def __init__(self) -> None:
        super().__init__(
            name=ConfigConst.MEM_UTIL_NAME, typeID=ConfigConst.MEM_UTIL_TYPE
        )

    def getTelemetryValue(self) -> float:
        return psutil.virtual_memory().percent
