from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket

def main():
	DetectCircles()
	# myCam = AnkerCamera(1) # Leave this commented out when the camera is not connected
	pi_bluetooth_socket = BluetoothServerSocket(10)



if __name__ == "__main__":
	main()