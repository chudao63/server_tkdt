
# import json
# import serial
# # import pyrebase
# from time import sleep
from email import message
from glob import escape
from random import random
from re import A
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# from threading import Thread
import time
import _thread
import random
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.config['MQTT_BROKER_URL'] = "broker.hivemq.com"
app.config['MQTT_BROKER_PORT'] = 1883


topic = "/quang_trinh_an_cut"
topic2 = "/quang_trinh_an_cut2"

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdate,flags,rc):
  if rc == 0:
    print("connect successfully") 
    mqtt_client.subscribe(topic)
    mqtt_client.subscribe(topic2)

  else:
    print("deo connect dc")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
  data = dict(topic = message.topic,
              payload = message.payload.decode()
              )
  print(data)



@app.route('/api/event', methods=['POST'])
def event():
    data = request.json
    emit('event', data, broadcast=True, namespace='/')
    return 'OK'


def background_thread():
    """Example of how to send server generated events to clients."""
   
    while True:
        time.sleep(0.1)
        socketio.emit('event',
                      {"Moment_1": random.randint(70, 100), "Moment_2":  random.randint(20, 50), "Moment_3": random.randint(1, 100),"Moment_4": random.randint(101, 299) },
                      namespace='/')

data = {
        "Moment_1": random.randint(70, 100), 
        "Moment_2":  random.randint(20, 50), 
        "Moment_3": random.randint(1, 100),
        "Moment_4": random.randint(101, 299)
       }

@app.route('/')
def index():
  return data

@app.route("/sensor")
def send_in4_sensor():
  return {"id": f"sensor_S0000{random.randint(1, 10)}","type": "sensor", "value": random.randint(20, 100), "unit": "percentage"}

@app.route("/scan")
def scan_sensor():
  mqtt_client.publish(topic=topic,payload = "scan_sensor")
  return "Scan sensor successfully"


if __name__ == '__main__':
  _thread.start_new_thread( background_thread, () )
  socketio.run(app)

