from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket


def main():

	# Initialize game variables
	Startup = True
	Current_Ball_List = None
	Previous_Ball_List = None

	# Initialize connections
	myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
	pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
	myCam.take_video()

	while(True):
		Startup = False

		# Begin computer vision
		myCam = AnkerCamera(2)
		myCam.take_picture() # 1 on Jetson Nano; 2 on laptop
		Current_Ball_List = DetectCircles()
		break



if __name__ == "__main__":
	main()
