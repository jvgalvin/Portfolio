import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt
import boto3
from botocore.exceptions import ClientError
import os
import datetime

REMOTE_MQTT_HOST="50.18.136.190" # Public IP address of EC2 VM
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="cam_bin_remote"
BUCKET = "jvgalvin-faces"

def on_connect_remote(remote_client, userdata, flags, rc):
    print("connected to cloud broker with rc: " + str(rc))
    remote_client.subscribe(REMOTE_MQTT_TOPIC)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print ("Error")
        return False
    return True

def on_message(client, userdata, msg):
    try:
        msg = msg.payload
        img_arr = np.frombuffer(msg, dtype=np.uint8)
        img_np = cv.imdecode(img_arr, cv.IMREAD_GRAYSCALE)
        f_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".png"
        cv.imwrite(f_name, img_np)
        upload_file(f_name, bucket=BUCKET, object_name=None)
    except:
        print ("Unexpected error:", sys.exc_info()[0])

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_message = on_message

remote_mqttclient.loop_forever()
