from src.ComputedShot import ComputedShot
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot
from src.BLE_Testing import Init_BLE
from src.ShotSelectionHelper import computeShot
from src import Settings

import time


def main():

	# Initialize game variables
	Startup = True
	Continue = False
	Current_Ball_List = None
	Previous_Ball_List = None

	Settings.InitializeGlobals()
	Init_BLE()
	print("Initialization Complete!")
	time.sleep(5)

	while True:
		#val = int(input("Enter number:"))
		#Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))
		#time.sleep(2)

		# Initialize connections
		# myCam = AnkerCamera(0) # 1 on Jetson Nano; 2 on laptop
		# pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
		# myCam.take_video()
		# myCam.take_picture()
		Current_Ball_List = DetectCircles()
		computedShot : ComputedShot = computeShot(Current_Ball_List=Current_Ball_List)
		break
			 
		if Previous_Ball_List is not None:
			try:
				ret = DetectShot(Previous_Ball_List, Current_Ball_List)
				# Need to add shot outcome logic in here
				print(ret)

			except InvalidBallCount:
				print("Invalid ball count, something is wrong")
			break
		# In here will be the user localization and guidance

		# Below is how to write a byte to the ESP32
		# Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))

		# Current shot is complete, store current game state
		# Current shot is complete, store current game state
		Previous_Ball_List = Current_Ball_List

		Startup = False

# CLEANUP myCam.shutdown()


if __name__ == "__main__":
	main()
