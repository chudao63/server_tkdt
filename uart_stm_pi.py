import json
import pyrebase
import serial
from time import sleep

fs = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate
FirebaseConfig = {
  "apiKey": "AIzaSyDHry-v-PilQJYo_GZTNRQYd4Q7RDswV3w",
  "authDomain": "raspberry-firebase-nodejs.firebaseapp.com",
  "databaseURL": "https://raspberry-firebase-nodejs-default-rtdb.firebaseio.com",
  "projectId": "raspberry-firebase-nodejs",
  "storageBucket": "raspberry-firebase-nodejs.appspot.com",
  "messagingSenderId": "661890992924",
  "appId": "1:661890992924:web:39615393ab8c234970c8d9",
  "measurementId": "G-YB1CDDYEN4"
}
firebase = pyrebase.initialize_app(FirebaseConfig)
database = firebase.database()

while True:
    received_data = fs.read()             #read serial port  
    sleep(0.018)
    data_left = fs.inWaiting()            #check for remaining byte
    received_data += fs.read(data_left)           
#    fs.write(received_data)    #Write to data  
    json_str = received_data.decode("utf-8", errors="replace")  
    print (json_str)
    print ("Data Da xử lí:")

    try:
      python_object = json.loads(json_str)    #Boc tách data json:
      object_mm1 = python_object["Moment_1"]
      object_mm2 = python_object["Moment_2"]
      object_mm3 = python_object["Moment_3"]
      object_mm4 = python_object["Moment_4"]
    except :
      print("Lỗi....")
      sleep(1)    #Chờ 1s sau để stm32 gửi về data mới.
      pass  







    print ("Moment 1: ",object_mm1)
    print ("Moment 2: ",object_mm2)
    print ("Moment 3: ",object_mm3)
    print ("Moment 4: ",object_mm4)


    database.child("Moment")
    data = {"Moment 1" : object_mm1,
            "Moment 2" : object_mm2,
            "Moment 3" : object_mm3,
            "Moment 4" : object_mm4 
            }
    database.set(data)
