from datetime import datetime, timezone

from forex_trading.common import ConfigConst


class BaseIotData:
    def __init__(
        self,
        name=ConfigConst.NOT_SET,
        typeID=ConfigConst.DEFAULT_TYPE_ID,
        d=None,
    ) -> None:
        self.updateTimeStamp()
        self.hasError = False

        useDefaults = True

        if d:
            try:
                self.name = d[ConfigConst.NAME_PROP]
                self.typeID = d[ConfigConst.TYPE_ID_PROP]
                self.statusCode = d[ConfigConst.STATUS_CODE_PROP]
                self.latitude = d[ConfigConst.LATITUDE_PROP]
                self.elevation = d[ConfigConst.LONGITUDE_PROP]

                useDefaults = False
            except Exception:
                pass

        if useDefaults:
            self.name = name
            self.typeID = typeID
            self.statusCode = ConfigConst.DEFAULT_STATUS
            self.latitude = ConfigConst.DEFAULT_LAT
            self.longitude = ConfigConst.DEFAULT_LON
            self.elevation = ConfigConst.DEFAULT_ELEVATION

        if not self.name:
            self.name = ConfigConst.NOT_SET

        # always pull location ID from configuration file
        self.locationID = ConfigConst.DEVICE_LOCATION_ID_KEY

    def statusCode(self, val: int):
        self.statusCode = val
        if val < 0:
            self.hasError = True

    def setLocationID(self, val: str):
        self.locationID = val

    def updateTimeStamp(self):
        self.timeStamp = str(datetime.now(timezone.utc).isoformat())

    def __str__(self):
        return f"""{ConfigConst.NAME_PROP}={self.name},
                   {ConfigConst.TYPE_ID_PROP}={self.typeID},
                   {ConfigConst.TIMESTAMP_PROP}={self.timeStamp},
                   {ConfigConst.STATUS_CODE_PROP}={self.statusCode},
                   {ConfigConst.HAS_ERROR_PROP}={self.hasError},
                   {ConfigConst.LOCATION_ID_PROP}={self.locationID},
                   {ConfigConst.ELEVATION_PROP}={self.elevation},
                   {ConfigConst.LATITUDE_PROP}={self.latitude},
                   {ConfigConst.LONGITUDE_PROP}={self.longitude}
        """
