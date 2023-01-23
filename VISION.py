from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot


def main():

	# Initialize game variables
	Startup = True
	Continue = True
	Current_Ball_List = None
	Previous_Ball_List = None

	# Initialize connections
	# myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
	# pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
	# myCam.take_video()

	while(Continue):
		
		# Begin computer vision
		# myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
		# myCam.take_picture()
		Current_Ball_List = DetectCircles()
		Previous_Ball_List = Current_Ball_List

		try:
			ret = DetectShot(Previous_Ball_List, Current_Ball_List)
			print(ret)
		except InvalidBallCount:
			print("Invalid ball count, something is wrong")
		break



if __name__ == "__main__":
	main()
