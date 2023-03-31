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
from src.MQTT_Localization import MQTT_Main

import time
import cv2
import threading
import paho.mqtt.client as mqtt
import threading
import paho.mqtt.client as mqtt

def main():

	# Initialize game variables
	Continue = False
	Current_Ball_List = None
	Previous_Ball_List = None
	Current_Position = None
	Target_Speakers = []
	Current_Speakers = []
	Guidance_Speakers = []
	

	#Initialize connections
	Settings.InitializeGlobals()
	myCam = AnkerCamera(-1)
	myCam.take_video()
	cv2.destroyAllWindows()
	Init_BLE()
	#mqttc = mqtt.Client(transport='websockets')   
	#mqttc.connect('broker.emqx.io', 8083, 60)
	#mqttc.subscribe("t/sd/feedback", 0)
	MQTT_Thread = threading.Thread(target = MQTT_Main)
	MQTT_Thread.start()
	time.sleep(5)
	print("Initialization Complete!")

	while True:
		for i in range(3):
		 	myCam.take_picture()

		Current_Ball_List = DetectCircles()
		computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		Target_Speakers = ConvertSSToSpeaker(computedShot.playerPos[0], computedShot.playerPos[1])
		Target_Speakers.sort()
		print("Final Target Speakers: " + str(Target_Speakers))

		while not UserArrived(Current_Speakers, Target_Speakers):

			# Get current position represented as speakers
			Settings.MQTT_Lock.acquire()
			if not Settings.MQTT_UpdateFlag:
				Settings.MQTT_Lock.release()
				time.sleep(1)
				continue
			else:
				Current_Speakers = Settings.MQTT_Speakers
				Settings.MQTT_UpdateFlag = False
				Settings.MQTT_Lock.release()

			# Get speakers to play and send them to the ESP32
			print("Take step towards speaker")
			Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
			print("Target speakers: " + str(Temp_Target_Speakers))
			SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)

		print("USER TAKE SHOT")
		break
		
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


if __name__ == "__main__":
	main()
