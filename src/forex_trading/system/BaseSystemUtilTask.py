class BaseSystemUtilTask:
    def __init__(self, name: str, typeID: int) -> None:
        self.name = name
        self.typeID = typeID

    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

    def getTelemetryValue(self) -> float:
        pass