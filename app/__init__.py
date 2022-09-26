from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mqtt import Mqtt
import logging
import coloredlogs
from flask_socketio import SocketIO, emit


coloredlogs.install(level='INFO', fmt = 'LOGGING: %(asctime)s %(levelname)s %(message)s' )

app =  Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:123456@localhost/thiet_ke_dien_tu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 20
db = SQLAlchemy(app)
CORS(app, support_credentials=True)

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

try:
    mqtt = Mqtt(app)
except:
    logging.error("Can't connect to MQTT Broker")