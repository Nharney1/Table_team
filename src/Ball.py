import cv2

# Need to define the thresholds for color here after experimented with them


class Ball(object):
	def __init__(self, x, y, radius, bgr):
		self.x = x
		self.y = y
		self.radius = radius
		self.bgr = bgr
		self.bgr_list = None
		self.color = None

	def 
