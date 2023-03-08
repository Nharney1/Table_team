import src.ShotSelection.run_single_production_mode as ShotSelectionProd
import src.ShotSelection.run_single_test_mode as ShotSelectionTest

from src.ShotSelection.pool_objets import Ball, CueBall, PoolPlayer
from src.ShotSelection.pool import Pool
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot
from src.Ball import BallConvertor
from src.ShotSelection.constants import Constants
from src.BLE_Testing import Init_BLE

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
		val = int(input("Enter number:"))
		Settings.noah_char.write_value(val.to_bytes(1,byteorder='big', signed=False))
		time.sleep(2)

		# Initialize connections
		# myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
		# pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
		# myCam.take_video()
		Current_Ball_List = DetectCircles()
  
		# Player 1 is solids and Player 2 is stripes
		playerTurn = PoolPlayer.PLAYER1
		playerTurn = PoolPlayer.PLAYER1
		pool = Pool(slowMotion=False, graphics=True)
		magnitudes = [45, 75, 90]
		angles = range(0, 360, 1)
  
		ballsProd = list()
				
		ppf = 195
		
		x_offset = Constants.WALL_THICKNESS
		y_offset = Constants.WALL_THICKNESS
		
		
		convertor = BallConvertor(ppf, x_offset, y_offset)
		
		cueBallProd = CueBall((0,0))
		
		for ball in Current_Ball_List:
			convertedBall = convertor.convertBall(ball)
			if convertedBall is not None:
				if convertedBall.number == 0:
					cueBallProd = convertedBall
				else:
					ballsProd.append(convertedBall)
		
	   
		ShotSelectionTest.runSingleTestMode(
			balls=ballsProd, 
			cueBall=cueBallProd, 
			magnitudes=magnitudes, 
			angles=angles, 
			pool_sim=pool, 
			turn=playerTurn
		  )
			

			 
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


if __name__ == "__main__":
	main()
