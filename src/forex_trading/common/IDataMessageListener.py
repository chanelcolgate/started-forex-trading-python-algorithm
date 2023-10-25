from forex_trading.data.SystemPerformanceData import SystemPerformanceData


class IDataMessageListener:
    def handleSystemPerformanceMessage(
        self, data: "SystemPerformanceData"
    ) -> bool:
        pass

    def setQueryQueue(self, query_queue):
        pass

    def getQueryQueue(self):
        pass

    def handleFixReceivedMessage(self, tickData):
        pass
