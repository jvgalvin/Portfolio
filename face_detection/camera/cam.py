# cam.py
# this is from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="10.43.225.173" 
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="cam_bin"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y:y+h, x:x+w]
        rc,png = cv.imencode('.png', face)
       # cv.imshow("frame", face)

        msg = png.tobytes()
        local_mqttclient.publish(LOCAL_MQTT_TOPIC,msg)

    # Display the resulting frame
    #cv.imshow('frame',face)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

