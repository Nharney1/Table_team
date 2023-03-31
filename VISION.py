from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetermineShotOutcome, GAME_BALL_MADE, OPPONENT_BALL_MADE, BLACK_AND_WHITE, BLACK_BEFORE_GAME_BALLS, BLACK_BALL_WINNER, SCRATCH, NOTHING
from src.BLEComms import InitBLE, SendCommand, SendCommandNoArgs, SEND_SPEAKERS, STOP_SPEAKERS
from src.ShotSelectionHelper import computeShot
from src.Speakers import DetermineNextSpeaker, ConvertSSToSpeaker, UserArrived
from src.MQTT_Localization import MQTT_Main, WALK_TO_SPEAKER, ROTATE_TO_SPEAKER

from src import Settings

import time
import cv2
import threading
import paho.mqtt.client as mqtt
import threading
import paho.mqtt.client as mqtt

def main():
	# Game variables
	Current_Ball_List = []
	Previous_Ball_List = []
	Current_Position = []
	Target_Speakers = []
	Current_Speakers = []
	Guidance_Speakers = []
	Swift_Commands = []
	Rotation_Speakers = []
	
	#Initialize connections
	Settings.InitializeGlobals()
	myCam = AnkerCamera(-1)
	myCam.take_video()
	cv2.destroyAllWindows()
	InitBLE()
	mqttc = mqtt.Client(transport='websockets')   
	mqttc.connect('broker.emqx.io', 8083, 60)
	mqttc.subscribe("t/sd/feedback", 0)
	MQTT_Thread = threading.Thread(target = MQTT_Main)
	MQTT_Thread.start()
	time.sleep(5)
	for i in range(3):
		 myCam.take_picture()
	Current_Ball_List = DetectCircles()
	print("Initialization Complete!")

	while True:
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
			Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
			print("Target speakers: " + str(Temp_Target_Speakers))
			SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)
			ret = mqttc.publish("t/sd/feedback", WALK_TO_SPEAKER)
			time.sleep(3)

		# User is in the correct location, now orient the user
		SendCommandNoArgs(STOP_SPEAKERS)
		ret  = mqttc.publish("t/sd/feedback", ROTATE_TO_SPEAKER)
		time.sleep(3)
		#Rotation_Speakers = AARON'S CODE TO DETERMINE SPEAKER 
		SendCommand(SEND_SPEAKERS, Rotation_Speakers)
		print("USER ROTATING")
		time.sleep(10)
		SendCommandNoArgs(STOP_SPEAKERS)
		##### SHOT IS TAKEN AT THIS POINT #####

		# Current shot is complete, store current game state
		Previous_Ball_List = Current_Ball_List
		for i in range(3):
			myCam.take_picture()
		Current_Ball_List =  DetectCircles()

		if not Previous_Ball_List:
			try:
				Swift_Commands = DetermineShotOutcome(Previous_Ball_List, Current_Ball_List)
				if len(Swift_Commands) ==  0:
					ret = mqttc.publish("t/sd/feedback", NOTHING)
				else:
					for command in Swift_Commands:
						ret= mqttc.publish("t/sd/feedback",commad)
						time.sleep(3)
			except InvalidBallCount:
				print("Invalid ball count, something is wrong")
			break
		cv2.destroyAllWindows()
		break

	myCam.shutdown()
	quit()

if __name__ == "__main__":
	main()
