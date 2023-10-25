##############################
# General Names and Defaults #
##############################

NOT_SET = "Not Set"
DEFAULT_HOST = "localhost"
DEFAULT_COAP_PORT = 5683
DEFAULT_COAP_SECURE_PORT = 5684
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_SECURE_PORT = 8883
DEFAULT_RTSP_STREAM_PORT = 8554
DEFAULT_KEEP_ALIVE = 60
DEFAULT_POLL_CYCLES = 60
DEFAULT_VAL = 0.0
DEFAULT_COMMAND = 0
DEFAULT_STATUS = 0
DEFAULT_TIMEOUT = 5
DEFAULT_TTL = 300
DEFAULT_QOS = 0

DEFAULT_LAT = DEFAULT_VAL
DEFAULT_LON = DEFAULT_VAL
DEFAULT_ELEVATION = DEFAULT_VAL

PRODUCT_NAME = "PIOT"
CLOUD = "Cloud"
GATEWAY = "Gateway"
CONSTRAINED = "Constrained"
DEVICE = "Device"
SERVICE = "Service"

CONSTRAINED_DEVICE = CONSTRAINED + DEVICE
GATEWAY_SERVICE = GATEWAY + SERVICE
CLOUD_SERVICE = CLOUD + SERVICE

LOCAL = "Local"
MQTT = "MQTT"
COAP = "Coap"
OPCUA = "Opcua"
SMTP = "Smtp"

############################
# Resource and Topic Names #
############################

ACTUATOR_CMD = "ActuatorCmd"
ACTUATOR_RESPONSE = "ActuatorResponse"
MGMT_STATUS_MSG = "MgmtStatusMsg"
MGMT_STATUS_CMD = "MgmStatusCmd"
SENSOR_MSG = "SensorMsg"
SYSTEM_PERF_MSG = "SystemPerfMsg"

LED_ACTUATOR_NAME = "LedActuator"
HUMIDIFIER_ACTUATOR_NAME = "HumidifierActuator"
HVAC_ACTUATOR_NAME = "HvacActuator"

HUMIDITY_SENSOR_NAME = "HumiditySensor"
PRESSURE_SENSOR_NAME = "PressureSensor"
TEMP_SENSOR_NAME = "TempSensor"
SYSTEM_PERF_NAME = "SystemPerfMsg"
CAMERA_SENSOR_NAME = "CameraSensor"
POWER_SENSOR_NAME = "PowerSensor"

COMMAND_OFF = DEFAULT_COMMAND
COMMAND_ON = 1

DEFAULT_TYPE_ID = 0
DEFAULT_ACTUATOR_TYPE = DEFAULT_TYPE_ID
HVAC_ACTUATOR_TYPE = 1
HUMIDIFIER_ACTUATOR_TYPE = 2
LED_DISPLAY_ACTUATOR_TYPE = 100

DEFAULT_SENSOR_TYPE = DEFAULT_TYPE_ID
HUMIDITY_SENSOR_TYPE = 1
PRESSURE_SENSOR_TYPE = 2
TEMP_SENSOR_TYPE = 3
POWER_SENSOR_TYPE = 4

SYSTEM_PERF_TYPE = 100
CPU_UTIL_TYPE = 101
DISK_UTIL_TYPE = 102
MEM_UTIL_TYPE = 103

CAMERA_SENSOR_TYPE = 200

CPU_UTIL_NAME = "DeviceCpuUtil"
DISK_UTIL_NAME = "DeviceDiskUtil"
MEM_UTIL_NAME = "DeviceMemUtil"

#############################################
# Configuration Sections, Keys and Defaults #
DEFAULT_CONFIG_FILE_NAME = "./config/PiotConfig.props"

CRED_FILE_KEY = "credFile"
CRED_SECTION = "Credentials"

POLL_CYCLES_KEY = "pollCycleSecs"
DEVICE_LOCATION_ID_KEY = "deviceLocationID"

ENABLE_SIMULATOR_KEY = "enableSimulator"
ENABLE_EMULATOR_KEY = "enableEmulator"
ENABLE_SENSE_HAT_KEY = "enableSenseHat"

HUMIDITY_SIM_FLOOR_KEY = "humiditySimFloor"
HUMIDITY_SIM_CEILING_KEY = "humiditySimCeiling"
PRESSURE_SIM_FLOOR_KEY = "pressureSimFloor"
PRESSURE_SIM_CEILING_KEY = "pressureSimCeiling"
TEMP_SIM_FLOOR_KEY = "tempSimFloor"
TEMP_SIM_CEILING_KEY = "temSimCeiling"

ENABLE_SYSTEM_PERF_KEY = "enableSystemPerformance"
ENABLE_SENSING_KEY = "enableSensing"

HANDLE_TEMP_CHANGE_ON_DEVICE_KEY = "handleTempChangeOnDevice"
TRIGGER_HVAC_TEMP_FLOOR_KEY = "triggerHvacTempFloor"
TRIGGER_HVAC_TEMP_CEILING_KEY = "triggerHvacTempCeiling"

CDA_SENSOR_DATA_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + SENSOR_MSG
)
CDA_ACTUATOR_CMD_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + ACTUATOR_CMD
)
CDA_ACTUATOR_RESPONSE_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + ACTUATOR_RESPONSE
)
CDA_MGMT_STATUS_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + MGMT_STATUS_MSG
)
CDA_MGMT_CMD_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + MGMT_STATUS_CMD
)
CDA_SYSTEM_PERF_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/" + SYSTEM_PERF_MSG
)
CDA_UPDATE_NOTIFICATIONS_MSG_RESOURCE = (
    PRODUCT_NAME + "/" + CONSTRAINED_DEVICE + "/TestUpdateMsg"
)
##################
# Property Names #
##################

NAME_PROP = "name"
TYPE_ID_PROP = "typeID"
TIMESTAMP_PROP = "timeStamp"
HAS_ERROR_PROP = "hasError"
STATUS_CODE_PROP = "statusCode"
LOCATION_ID_PROP = "locationID"
LATITUDE_PROP = "latitude"
LONGITUDE_PROP = "longitude"
ELEVATION_PROP = "elevation"

UPDATE_NOTIFICATIONS_MSG = "updatemsg"

COMMAND_PROP = "command"
STATE_DATA_PROP = "stateData"
VALUE_PROP = "value"
IS_RESPONSE_PROP = "isResponse"

CPU_UTIL_PROP = "cpuUtil"
DISK_UTIL_PROP = "diskUtil"
MEM_UTIL_PROP = "memUtil"

RUN_FOREVER_KEY = "runForever"

#########################################
# MQTT client configuration information #
#########################################
MQTT_GATEWAY_SERVICE = MQTT + "." + GATEWAY_SERVICE

HOST_KEY = "host"
PORT_KEY = "port"
SECURE_PORT_KEY = "securePort"
DEFAULT_QOS_KEY = "defaultQos"
KEEP_ALIVE_KEY = "keepAlive"

ENABLE_MQTT_CLIENT_KEY = "enableMqttClient"

##################################
# COAP configuration information #
#################################

ENABLE_COAP_CLIENT_KEY = "enableCoapClient"
ENABLE_COAP_SERVER_KEY = "enableCoapServer"

COAP_GATEWAY_SERVICE = COAP + "." + GATEWAY_SERVICE