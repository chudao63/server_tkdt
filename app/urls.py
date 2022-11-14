from app import api1
from app.api import *

api1.add_resource(
    ScanSensor,
    "/scan_sensor"
)
api1.add_resource(
    ReadDataSensor,
    "/data_sensor"
)
api1.add_resource(
    ReadGateway,
    "/gateway"
)
api1.add_resource(
    ReadDataGateway,
    "/data_gateway"
)
api1.add_resource(
    Test,
    "/"
)
api1.add_resource(
    CreateGateWay,
    "/create_gateway"
)

api1.add_resource(
    ReadDataGatewayByIdSensor,
    "/get_data_by_id"
)

api1.add_resource(
    SettimeTimeSensor,
    "/set_time"
)


api1.add_resource(
    DeleteSensor,
    "/delete_sensor"
)
