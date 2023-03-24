import sys
import json
import paho.mqtt.client as mqtt
import csv
import time
import numpy as np 
import math


def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(str(msg.payload.decode("utf-8"))) #messages received are printed from here
               
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)
    
#time.sleep(10)
mqttc = mqtt.Client(transport='websockets')   
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect('broker.emqx.io', 8083, 60)
mqttc.subscribe("t/sd/scratch", 0)
#mqttc.subscribe("$SYS/#", 0)
ret= mqttc.publish("t/sd/scratch","start") #use this line to send
mqttc.loop_forever()
