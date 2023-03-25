from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot
from src.BLE_Testing import Init_BLE
from src.ShotSelectionHelper import computeShot
from src.Speakers import DetermineNextSpeaker

from src import Settings
from src.MQTT_Localization import MQTT_Main

import time
import cv2
import threading
import paho.mqtt.client as mqtt

def main():

	# Initialize game variables
	Startup = True
	Continue = False
	Current_Ball_List = None
	Previous_Ball_List = None
	temp_current_position = None
	

	#Initialize connections
	Settings.InitializeGlobals()
	#Init_BLE()
	myCam = AnkerCamera(0) # 1 on Jetson Nano; 2 on laptop
	#pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)

	#myCam.take_video()
	#cv2.destroyAllWindows()
	mqttc = mqtt.Client(transport='websockets')   
	mqttc.connect('broker.emqx.io', 8083, 60)
	mqttc.subscribe("t/sd/feedback", 0)
	MQTT_Thread = threading.Thread(target = MQTT_Main)
	MQTT_Thread.start()
	#pi_bluetooth_socket.initServerSocket()
	myCam.take_video()
	cv2.destroyAllWindows()
	print("Initialization Complete!")
	time.sleep(2)

	while True:
		#print("sleeping")
		#time.sleep(1)
		#val = int(input("Enter number: "))
		#Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))
		#time.sleep(2)
		for i in range(10):
			myCam.take_picture()

		#Current_Ball_List = DetectCircles()
		#computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		
			
		#if Previous_Ball_List is not None:
			#try:
				#ret = DetectShot(Previous_Ball_List, Current_Ball_List)
				# Need to add shot outcome logic in here
				#print(ret)

			#except InvalidBallCount:
				#print("Invalid ball count, something is wrong")
			#break
		# In here will be the user localization and guidance

		print("VISION sleeping")
		time.sleep(1)

		Settings.MQTT_Lock.acquire()
		temp_current_position = Settings.MQTT_Location
		print(temp_current_position)
		Settings.MQTT_Lock.release()
		
		# Below is how to write a byte to the ESP32
		# Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))

		# Current shot is complete, store current game state
		#Previous_Ball_List = Current_Ball_List

		#Startup = False

		shot_result_feedback = 0
		ret= mqttc.publish("t/sd/feedback",shot_result_feedback)   
		#for i in range(20):
			#print('Sleeping')
			#time.sleep(1)
		#cv2.destroyAllWindows()

# CLEANUP myCam.shutdown()


if __name__ == "__main__":
	main()
