from app import mqtt
import logging
from app import db
from app.parse import parse_body_data
from app.models import Sensor, GateWay, DataSensor
from app.result_sensor import RESULT
from app.vntime import *
from datetime import datetime
from flask_socketio import SocketIO, emit
from app import app
from flask import current_app

flag = 0
result_scan_sensor = {}


def scan_sensor(data):
    name_sensor = data['scan_sensor'].get("mac_sensor")
    name_gateway = data['scan_sensor'].get("mac_gateway")

    data_gateway = GateWay.query.filter(GateWay.name == name_gateway).one()

    for sensor in data_gateway.sensors:
        if name_sensor == sensor.__dict__.get("name"):
            return {"message": "Not found new sensor"}

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
    insert_data_sensor(data)
    return data


def insert_data_sensor(data):
    try:
        name_sensor = data['get_data_sensor'].get("mac_sensor")
        now = datetime.now()
        timeStamp = now.timestamp()
        timeNow = VnTimestamp.get_date_time_str(timeStamp)
        id_sensor = (Sensor.query.filter(Sensor.name == name_sensor).one().__dict__).get("id")
        insert_data = DataSensor(id_sensor=id_sensor, type_sensor=data["get_data_sensor"]["type_sensor"],
                                 type_device=data["get_data_sensor"]["type_device"], value=data['get_data_sensor'].get("value"),
                                 unit=data["get_data_sensor"]["unit"],
                                 battery=data["get_data_sensor"]["battery"], create_at=timeNow)
        db.session.add(insert_data)
        db.session.commit()
    except:
        logging.info("Loi insert data")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("/result_scan")
    logging.info("CONNECTED TO MQTT")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    rawData = message.payload.decode('utf-8')
    payload = parse_body_data(rawData)
    logging.info(f"{message.topic}: {payload}")

    if "scan_sensor" in payload:
        result_scan_sensor = scan_sensor(payload)
        logging.info(result_scan_sensor)
        with app.app_context():
            emit('scan_sensor', result_scan_sensor, broadcast=True, namespace='/')

    # if "scan_gateway" in payload:
    #     if not (GateWay.query.filter(GateWay.name == payload['scan_gateway']['mac_address']).all()):
    #         insert_gateway = GateWay(name=payload["scan_gateway"]["mac_address"])
    #         db.session.add(insert_gateway)
    #         db.session.commit()
    #         with app.app_context():
    #             emit('scan_gateway', payload["scan_gateway"], broadcast=True, namespace='/')
    #     else:
    #         with app.app_context():
    #             logging.info("không tìm thấy gateway mới")
    #             emit('scan_gateway', "không tìm thấy gateway mới", broadcast=True, namespace='/')

    if "get_data_sensor" in payload:
        insert_data_sensor(payload)
        with app.app_context():
            emit('data_sensor', payload["get_data_sensor"], broadcast=True, namespace='/')