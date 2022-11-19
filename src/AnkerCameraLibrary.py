import cv2, os

class AnkerCamera(object):
	def __init__(self, port):
		self.cam_port = port
		self.cam = cv2.VideoCapture(self.cam_port, cv2.CAP_DSHOW)


	def take_picture(self):
		if not self.cam.isOpened():
			print('Cannot open camera')
			exit()

		result, image = self.cam.read() # Flush the inital contents of the camera
		result, image = self.cam.read()

		if not result:
			print('Cannot capture image')
		else:
			cv2.imshow('Sample image', image)
			cv2.imwrite('C:/Users/UHSgi/Desktop/SD_scripts/cv/test_image.png', image)
			cv2.waitKey(0)

	def take_video(self):
		if not self.cam.isOpened():
			print('Cannot open camera')
			exit()

		while True:
			i = 0
			result, image = self.cam.read()
			cv2.imshow('video', image)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.shutdown()
				break


	def shutdown(self):
		self.cam.release()
		cv2.destroyAllWindows()