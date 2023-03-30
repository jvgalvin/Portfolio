# forwarder.py
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="cam_bin"

REMOTE_MQTT_HOST="50.18.136.190" # Public IP of EC2 VM
REMOTE_MQTT_PORT=1883 # Remote host listening on 1883
REMOTE_MQTT_TOPIC="cam_bin_remote"

def on_connect_local(local_client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    local_client.subscribe(LOCAL_MQTT_TOPIC)

def on_connect_remote(remote_client, userdata, flags, rc):
    print("conneted to remote broker with rc: " + str(rc))
    remote_client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  try:
    msg = msg.payload
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_message = on_message

# go into a loop
remote_mqttclient.loop_start()
local_mqttclient.loop_forever()


#local_mqttclient.loop_forever()
#remote_mqttclient.loop_forever()
