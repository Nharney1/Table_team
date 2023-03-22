from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot
from src.BLE_Testing import Init_BLE
from src.ShotSelectionHelper import computeShot
from src import Settings

import time
import cv2
import sys
import json
import paho.mqtt.client as mqtt
import csv
import time
import numpy as np 
import math

actionsignal = False

def on_connect(mqttc, obj, flags, rc):
    	print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
	msg = str(msg.payload.decode("utf-8")) #messages received are printed from here
	if msg == 'start':
		actionsignal = True
	if msg == 'stop':
		actionsignal = True

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
mqttc.subscribe("t/sd/vision", 0)
#mqttc.subscribe("$SYS/#", 0)
#ret= mqttc.publish("t/sd/scratch","start") #use this line to send
mqttc.loop_forever()


def main():

	# Initialize game variables
	Startup = True
	Continue = False
	Current_Ball_List = None
	Previous_Ball_List = None


	#Initialize connections
	Settings.InitializeGlobals()
	#Init_BLE()
	#myCam = AnkerCamera(0) # 1 on Jetson Nano; 2 on laptop
	#pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
	#myCam.take_video()
	#cv2.destroyAllWindows()
	print("Initialization Complete!")

	while True:
		#val = int(input("Enter number:"))
		#Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))
		#time.sleep(2)
		#for i in range(10):
		#	myCam.take_picture()

		Current_Ball_List = DetectCircles()
		computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		
		if actionsignal:
			with open('targetposition.csv', 'w') as f:
			    writer = csv.writer(f)
			    writer.writerow([computedShot.playerPos[0], computedShot.playerpos[1]])			
			
		#if Previous_Ball_List is not None:
			#try:
				#ret = DetectShot(Previous_Ball_List, Current_Ball_List)
				# Need to add shot outcome logic in here
				#print(ret)

			#except InvalidBallCount:
				#print("Invalid ball count, something is wrong")
			#break
		# In here will be the user localization and guidance

		# Below is how to write a byte to the ESP32
		# Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))

		# Current shot is complete, store current game state
		# Current shot is complete, store current game state
		#Previous_Ball_List = Current_Ball_List

		#Startup = False

		for i in range(20):
			print('Sleeping')
			time.sleep(1)
		cv2.destroyAllWindows()

# CLEANUP myCam.shutdown()


if __name__ == "__main__":
	main()
