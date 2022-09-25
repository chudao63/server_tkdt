from app import mqtt
import logging
from app import db
from app.parse import parse_body_data
from app.models import Sensor, GateWay
from app.result_sensor import RESULT
from app.vntime import *
from datetime import datetime

flag = 0
result_scan_sensor = {}
def scan_sensor(data):
    name_sensor = data.get("name_sensor")
    name_gateway = data.get("name_gateway")
    data_gateway = GateWay.query.filter(GateWay.name == name_gateway).one()
    for sensor in data_gateway.sensors:
        if name_sensor == sensor.__dict__.get("name"):
            return {"message":"Not found new sensor"}
    if (Sensor.query.filter(Sensor.name == name_sensor).all()):
        data_sensor = Sensor.query.filter(Sensor.name == name_sensor).one()
    else:
        add_sensor = Sensor(name=name_sensor)
        db.session.add(add_sensor)
        db.session.commit()
        data_sensor = Sensor.query.order_by(Sensor.id.desc()).first()
    data_gateway.sensors.append(data_sensor)
    db.session.add(data_gateway)
    db.session.commit()
    return data


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    pass
    # mqtt.subscribe("/tkdt/read_data_sensor")
    mqtt.subscribe("/tkdt/scan_sensor")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    pass

    # global result_scan_sensor, flag
    # rawData = message.payload.decode('utf-8')
    # payload = parse_body_data(rawData)
    # #socketio
    # if "scan" in payload:
    #     result_scan_sensor = scan_sensor(payload['scan'])
    #     flag = 1




