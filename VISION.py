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

def  on_connect_PI(mqttc, obj, flags, rc):
	print("rc: "  +  str(rc))

def on_message_PI(mqttc, obj, msg):
	print("PI msg: " +  str(msg.payload.decode("utf-8")))
	Settings.waitingOnScratch  = False

def on_publish_PI(mqttc, obj, mid):
	print("mid: " +  str(mid))

def on_subscribe_PI(mqttc, obj, mid, granted_qos):
	print("Subscribed")

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
	Temp_Target_Speakers = []
	
	#Initialize connections
	Settings.InitializeGlobals()
	mqttc = mqtt.Client(transport='websockets')   
	mqttc.connect('broker.emqx.io', 8083, 60)
	mqttc.subscribe("t/sd/feedback", 0)
	mqtt_PI = mqtt.Client(transport='websockets')
	mqtt_PI.on_message = on_message_PI
	mqtt_PI.on_publish = on_publish_PI
	mqtt_PI.on_subscribe = on_subscribe_PI
	mqtt_PI.connect('broker.emqx.io', 8083, 60)
	mqtt_PI.subscribe("t/sd/scratch", 0)
	mqtt_PI.loop_start()
	time.sleep(2)
	MQTT_Thread = threading.Thread(target = MQTT_Main)
	MQTT_Thread.start()
	Current_Ball_List = DetectCircles()
	print("Initialization Complete!")

	while True:
		computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		Target_Speakers = ConvertSSToSpeaker(computedShot.playerPos[0], computedShot.playerPos[1])
		Target_Speakers.sort()
		print("Final Target Speakers: " + str(Target_Speakers))
		break
		while True:
			# Get current position
			Settings.MQTT_Lock.acquire()
			if Settings.MQTT_UpdateFlag:
				Current_Speakers = Settings.MQTT_Speakers.copy()
				Settings.MQTT_UpdateFlag = False
				print("Updated current speakers")
			Settings.MQTT_Lock.release()

			if UserArrived(Current_Speakers, Target_Speakers):
				print("ARRIVED AT FINAL")
				break
			else:
				if UserArrived(Current_Speakers, Temp_Target_Speakers):
					print("ARRIVED AT TEMP")
				Temp_Target_Speakers = DetermineNextSpeaker(Current_Speakers, Target_Speakers)
				print("Temp target speakers: " + str(Temp_Target_Speakers))
				SendCommand(SEND_SPEAKERS, Temp_Target_Speakers)
				mqttc.publish("t/sd/feedback", WALK_TO_SPEAKER)
				time.sleep(3)
		time.sleep(3)
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
