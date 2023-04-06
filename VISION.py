import time
import cv2
import threading
import sys
import paho.mqtt.client as mqtt

from src import Settings
from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.ShotSelectionHelper import computeShot

from src.BLEComms import (InitBLE,
						  SendCommand,
						  SendCommandNoArgs,
						  SEND_SPEAKERS,
						  STOP_SPEAKERS)

from src.Speakers import (DetermineNextSpeaker,
						  ConvertSSToSpeaker,
						  UserArrived,
						  DetermineAngleSpeaker)

from src.GameState import (InvalidBallCount,
						   DetermineShotOutcome,
						   GAME_BALL_MADE,
						   OPPONENT_BALL_MADE,
						   BLACK_AND_WHITE,
						   BLACK_BEFORE_GAME_BALLS,
						   BLACK_BALL_WINNER,
						   SCRATCH,
						   NOTHING)

from src.MQTT_Localization import (MQTT_Main,
								   WALK_TO_SPEAKER,
								   ROTATE_TO_SPEAKER)

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
	Angle_Speakers = []
	Temp_Target_Speakers  = []
	
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

		# cont = True
		# while cont:
		# 	if UserArrived(Current_Speakers, Target_Speakers):
		# 		cont = False
		# 		break
		# 	while not UserArrived(Current_Speakers, Temp_Target_Speakers):
		# 		# Get current speakers
		# 		Settings.MQTT_Lock.acquire()
		# 		Current_Speakers = Settings.MQTT_Speakers
		# 		Settings.MQTT_UpdateFlag = False
		# 		Settings.MQTT_Lock.release()

		# 		Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
		# 		print("Temp target speakers: " + str(Temp_Target_Speakers))
		# 		SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)
		# 		mqttc.publish("t/sd/feedback", WALK_TO_SPEAKER)
		# 		time.sleep(4)
		# 		break

		while not UserArrived(Current_Speakers, Target_Speakers):
			# Get current position represented as speakers
			Settings.MQTT_Lock.acquire()
			if not Settings.MQTT_UpdateFlag:
				Settings.MQTT_Lock.release()
				# time.sleep(1)
				# continue
			else:
				Current_Speakers = Settings.MQTT_Speakers
				Settings.MQTT_UpdateFlag = False
				Settings.MQTT_Lock.release()

			# Get speakers to play and send them to the ESP32
			Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
			print("Temp target speakers: " + str(Temp_Target_Speakers))
			SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)
			mqttc.publish("t/sd/feedback", WALK_TO_SPEAKER)
			time.sleep(4)


		time.sleep(2)
		# User is in the correct location, now orient the user
		SendCommandNoArgs(STOP_SPEAKERS)
		mqttc.publish("t/sd/feedback", ROTATE_TO_SPEAKER)
		time.sleep(3)
		Rotation_Speakers = DetermineAngleSpeaker(Current_Speakers, computedShot)
		print(Rotation_Speakers)
		SendCommand(SEND_SPEAKERS, Rotation_Speakers)
		time.sleep(10)
		SendCommandNoArgs(STOP_SPEAKERS)
		##### SHOT IS TAKEN AT THIS POINT #####
		for i in range(15):
			time.sleep(1)
			print("Taking shot")
		# Current shot is complete, store current game state
		Previous_Ball_List = Current_Ball_List
		for i in range(3):
			myCam.take_picture()
		Current_Ball_List =  DetectCircles()
		print("Detecting circles")
		if Previous_Ball_List:
			print("Here")
			try:
				Swift_Commands = DetermineShotOutcome(Previous_Ball_List, Current_Ball_List)
				if len(Swift_Commands) ==  0:
					mqttc.publish("t/sd/feedback", NOTHING)
				else:
					for command in Swift_Commands:
						mqttc.publish("t/sd/feedback",command)
						time.sleep(3)
				if BLACK_BALL_WINNER  in  Swift_Commands:
					SendCommandNoArgs(STOP_SPEAKERS)
					sys.exit()
			except InvalidBallCount:
				print("Invalid ball count, something is wrong")

	myCam.shutdown()
	quit()

if __name__ == "__main__":
	main()
