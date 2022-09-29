from app import mqtt
import logging
from app import db
from app.parse import parse_body_data
from app.models import Sensor, GateWay
from app.result_sensor import RESULT
from app.vntime import *
from datetime import datetime
from flask_socketio import SocketIO, emit
from app import  app
from flask import current_app
flag = 0
result_scan_sensor = {}
def scan_sensor(data):
    name_sensor = data['get_data_sensor'].get("mac_address")
    name_gateway = data['get_data_sensor'].get("mac_gateway")
    print(data)
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
    mqtt.subscribe("/result_scan")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    rawData = message.payload.decode('utf-8')
    payload = parse_body_data(rawData)
    logging.info(f"{message.topic}: {payload}")
    logging.info(payload)


    if "get_data_sensor" in payload:
        # if  payload['scan_sensor'] == "sensor has already existed":
        #     with app.app_context():
        #         emit('event', "sensor has already existed", broadcast=True, namespace='/')
        # else:
        result_scan_sensor = scan_sensor(payload)
        logging.info(result_scan_sensor)
        with app.app_context():
            emit('event', result_scan_sensor, broadcast=True, namespace='/')

    if "scan_gateway" in payload:
        if not (GateWay.query.filter(GateWay.name == payload['scan_gateway']['mac_address']).all()):
            insert_gateway = GateWay(name = payload["scan_gateway"]["mac_address"])
            db.session.add(insert_gateway)
            db.session.commit()
        else:
            logging.info("Không có gate way mới")





