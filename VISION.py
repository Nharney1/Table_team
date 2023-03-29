from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetermineShotOutcome
from src.BLEComms import Init_BLE, SendCommand, SEND_SPEAKERS
from src.ShotSelectionHelper import computeShot
from src.Speakers import DetermineNextSpeaker, ConvertSSToSpeaker, UserArrived

from src import Settings
from src.MQTT_Localization import MQTT_Main

import time
import cv2
import threading
import paho.mqtt.client as mqtt

def main():

	# Initialize game variables
	Continue = False
	Current_Ball_List = None
	Previous_Ball_List = None
	Current_Position = None
	Target_Speakers = []
	Temp_Target_Speakers = []
	Current_Speakers = []
	

	#Initialize connections
	Settings.InitializeGlobals()
	#Init_BLE()
	#mqttc = mqtt.Client(transport='websockets')   
	#mqttc.connect('broker.emqx.io', 8083, 60)
	#mqttc.subscribe("t/sd/feedback", 0)
	#MQTT_Thread = threading.Thread(target = MQTT_Main)
	#MQTT_Thread.start()
	#myCam = AnkerCamera(0) # 1 on Jetson Nano; 2 on laptop
	#myCam.take_video()
	#cv2.destroyAllWindows()
	#print("Initialization Complete!")
	#time.sleep(2)

	while True:
		# for i in range(3):
		# 	myCam.take_picture()

		Current_Ball_List = DetectCircles()
		computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		Target_Speakers = ConvertSSToSpeaker(computedShot.playerPos[0], computedShot.playerPos[1])
		Target_Speakers.sort()

		while not UserArrived(Current_Speakers, Target_Speakers):
			
			# Get the newest speaker location if available
			Settings.MQTT_Lock.acquire()
			if not Settings.Flag:
				Settings.MQTT_Lock.release()
				time.sleep(1)
				continue
			else:
				Current_Speakers = Settings.MQTT_Speakers
				Settings.Flag = False
				Settings.MQTT_Lock.release()

			# Get speakers to play and send them to the ESP32
			Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
			SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)

		
		#if Previous_Ball_List is not None:
			#try:
				#ret = DetermineShotOutcome(Previous_Ball_List, Current_Ball_List)
				# Need to add shot outcome logic in here
				#print(ret)

			#except InvalidBallCount:
				#print("Invalid ball count, something is wrong")
			#break

		# Current shot is complete, store current game state
		#Previous_Ball_List = Current_Ball_List

		#shot_result_feedback = 0
		#ret= mqttc.publish("t/sd/feedback",shot_result_feedback)   
		#for i in range(20):
			#print('Sleeping')
			#time.sleep(1)

		#cv2.destroyAllWindows()

# CLEANUP myCam.shutdown()


# Below is how to write a byte to the ESP32
# Settings.esp_char.write_value(val.to_bytes(1,byteorder='big', signed=False))

if __name__ == "__main__":
	main()
