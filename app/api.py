import json
from datetime import datetime
from flask_socketio import emit
from app.models import GateWay, Sensor, DataSensor
from flask_restful import Resource, Api, request, reqparse
from app import db, mqtt, socketio,api, app
from app.vntime import VnTimestamp

class CreateGateWay(Resource):
    def post(self):
        data = request.get_json(force=True)
        create_gateway = GateWay(name = data['name'])
        db.session.add(create_gateway)
        db.session.commit()
        return("Add gateway susscessful")


class ReadGateway(Resource):
    def get(self):
        """
        Lấy tất cả các gateway đang có
        """
        res = []
        gateways = GateWay.query.all()
        for gateway in gateways:
            gatewayDict = gateway.__dict__
            gatewayDict.pop("_sa_instance_state")
            gatewayDict.pop("sensors")
            res.append(gatewayDict)
        return res

    def post(self):
        mqtt.publish("/scan", payload='{"action": "scan_gateway"}')



class ReadDataGateway(Resource):
    def post(self):
        """
        Lấy data từ các sensor thuộc gateway
        body: {
            "gateway_name": "string",
            "sensor_name": "string
        }
        """
        res = {}
        data = request.get_json(force=True)
        gateways = GateWay.query.filter(GateWay.name == data.get("gateway_name")).one()
        if "sensor_name" in data:
            for sensor_gateway in gateways.sensors:
                if (sensor_gateway.name == data.get("sensor_name")):
                    data_sensors = DataSensor.query.filter(DataSensor.id_sensor == sensor_gateway.id).order_by(
                        DataSensor.id.desc()).limit(10).all()
            list_data_sensor = []
            list_time_data_sensor = []
            for data_sensor in data_sensors:
                data_sensor_dict = data_sensor.__dict__
                data_sensor_dict.pop("_sa_instance_state")
                list_data_sensor.append(data_sensor_dict.get("value"))
                list_time_data_sensor.append(data_sensor_dict.get("create_at"))
            res.update({data.get("gateway_name"): {
                data.get("sensor_name"): {"value": list_data_sensor, "time": list_time_data_sensor}}})
            return res

class ReadDataGatewayByIdSensor(Resource):
    def get(self):
        """
        Lấy data từ các sensor id
        params: id: id sensor
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        res = []
        data_sensors = DataSensor.query.filter(DataSensor.id_sensor == args['id']).order_by(DataSensor.id.desc()).limit(10).all()
        for data_sensor in data_sensors:
            data_sensor_dict = data_sensor.__dict__
            data_sensor_dict.pop("_sa_instance_state")
            res.append({"value": data_sensor_dict.get("value"), "time":data_sensor_dict.get("create_at") })
        return {"data": res}

class SettimeTimeSensor(Resource):
    data = request.get_json(force=True)
    print()

class ScanSensor(Resource):
    def get(self):
        """
        Lấy tất cả các sensor đã được scan
        """
        response = []
        sensors = Sensor.query.order_by(Sensor.id.asc()).all()
        for sensor in sensors:
            sensorDict = sensor.__dict__
            sensorDict.pop("_sa_instance_state")
            sensorDict.pop("gateways")
            response.append(sensorDict)
        return response

    def post(self):
        """
        Scan sensor mới
        """
        data = request.get_json(force=True)
        name_gateway = data.get("name_gateway")
        # data_gateway = GateWay.query.filter(GateWay.name == name_gateway).one()
        # for sensor in data_gateway.sensors:
        #     if name_sensor == sensor.__dict__.get("name"):
        #         return {"message": "Not found new sensor"}
        # if (Sensor.query.filter(Sensor.name == name_sensor).all()):
        #     data_sensor = Sensor.query.filter(Sensor.name == name_sensor).one()
        # else:
        #     add_sensor = Sensor(name=name_sensor)
        #     db.session.add(add_sensor)
        #     db.session.commit()
        #     data_sensor = Sensor.query.order_by(Sensor.id.desc()).first()
        # data_gateway.sensors.append(data_sensor)
        # db.session.add(data_gateway)
        # db.session.commit()
        # return data
        data_publish = {"action": "scan_sensor", "name_gateway": name_gateway}
        mqtt.publish("/scan", payload= json.dumps(data_publish))
        # emit('event', "hello", broadcast=True, namespace='/')

class Test(Resource):
    def get(self):
        with app.app_context():
            emit('event', "hello", broadcast=True, namespace='/')
        return "HELLO WORLD"



class ReadDataSensor(Resource):
    def get(self):
        """
        Lấy tất cả data đang có
        """
        res = []
        read_data = DataSensor.query.order_by(
                        DataSensor.id.desc()).limit(10).all()
        for data in read_data:
            dataDict = data.__dict__
            dataDict.pop("_sa_instance_state")
            res.append(dataDict)
        return res

    def post(self):
        """
        Thêm data đọc được vào bảng DataSensor
        body: {
                "sensor": "string",
                "value": float,
                "unit": "string",
                "battery": float
            }
        """
        now = datetime.now()
        timeStamp = now.timestamp()
        timeNow = VnTimestamp.get_date_time_str(timeStamp)
        data = request.get_json(force=True)
        id_sensor = (Sensor.query.filter(Sensor.name == data.get("sensor")).one().__dict__).get("id")
        insert_data = DataSensor(id_sensor=id_sensor, value=data.get("value"), unit=data.get("unit"),
                                 battery=data.get("battery"), create_at=timeNow)
        db.session.add(insert_data)
        db.session.commit()
        return "Thêm mới thành công"


api.add_resource(
    ScanSensor,
    "/scan_sensor"
)
api.add_resource(
    ReadDataSensor,
    "/data_sensor"
)
api.add_resource(
    ReadGateway,
    "/gateway"
)
api.add_resource(
    ReadDataGateway,
    "/data_gateway"
)
api.add_resource(
    Test,
    "/"
)
api.add_resource(
    CreateGateWay,
    "/create_gateway"
)

api.add_resource(
    ReadDataGatewayByIdSensor,
    "/get_data_by_id"
)
""" Long
    Body1:    {"id_sensor": string, "delete": bool}
    Body2:    {"id_sensor": string, "set_time": int}
"""

"""
    1, Scan sensor: data, {"unit_card": string, "delete": bool - fix = 0, "set_time": int - fix}
    2, mess:{"data_setting": {"unit_card": string, "delete": bool, "set_time": int}}
"""