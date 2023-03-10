from enum import Enum
import cv2 as cv

# Define the minimum and maximum coordinates for the billiard balls
X_MIN = 60
X_MAX = 1150
Y_MIN = 25
Y_MAX = 570
ERROR = 12

# Color thresholds
WHITE_BALL = 225
COLOR_BALL = 140

class BallColor(Enum):
    WHITE = 'white'
    BLACK = 'black'
    GREEN = 'green'
    BLUE = 'blue'
    
class Ball(object):
    
	def __init__(self, x, y, radius):
		self.x_hidden = x
		self.y_hidden = y
		self.x = x - X_MIN
		self.y = y - Y_MIN
		self.radius = radius
		self.blue = None
		self.green = None
		self.red = None
		self.color = None

	def CleanBGRVector(self, img):

		# Define a sampling interval
		intervals = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
		samples = len(intervals) * len(intervals)

		# Initial BGR values for each ball
		blue = 0
		green = 0
		red = 0

		for i in range (len(intervals)):
			for j in range (len(intervals)):
				blue += img[self.y_hidden + intervals[j], self.x_hidden + intervals[i]][0]
				green += img[self.y_hidden + intervals[j], self.x_hidden + intervals[i]][1]
				red += img[self.y_hidden + intervals[j], self.x_hidden + intervals[i]][2]

		# Update each balls color
		self.blue = int(blue/samples)
		self.green = int(green/samples)
		self.red = int(red/samples)


	def SetColor(self):
		if self.blue >= WHITE_BALL and self.green >= WHITE_BALL and self.red >= WHITE_BALL:
			self.color = BallColor.WHITE
		elif self.blue <= COLOR_BALL and self.green <= COLOR_BALL and self.red <= COLOR_BALL:
			self.color = BallColor.BLACK
		elif self.blue > self.green:
			self.color = BallColor.BLUE
		else:
			self.color = BallColor.GREEN
