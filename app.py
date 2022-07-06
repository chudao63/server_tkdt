
# import json
# import serial
# # import pyrebase
# from time import sleep
from random import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# from threading import Thread
import time
import _thread
import random
# __all__ = ("error", "LockType", "start_new_thread", "interrupt_main", "exit", "allocate_lock", "get_ident", "stack_size", "acquire", "release", "locked")

# eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


fs = {"Moment_1": 34, "Moment_2": 45, "Moment_3": 10,"Moment_4": 98 }

object_mm1 = fs["Moment_1"]
object_mm2 = fs["Moment_2"]
object_mm3 = fs["Moment_3"]
object_mm4 = fs["Moment_4"]

data = {"Moment 1" : object_mm1,
        "Moment 2" : object_mm2,
        "Moment 3" : object_mm3,
        "Moment 4" : object_mm4 
        }
@socketio.on('vehicle message')
def broadcast_vehicle(data):
    print(data)
    emit('vehicles', data, broadcast=True)


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
@app.route('/')
def index():
  _thread.start_new_thread( background_thread, () )
  return render_template('monitor.html')

if __name__ == '__main__':
  socketio.run(app)

