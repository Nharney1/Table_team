from enum import Enum
import cv2 as cv
from src.ShotSelection.pool_objets  import Ball as aiBall
from src.ShotSelection.pool_objets  import CueBall as aiCueBall
from src.ShotSelection.constants  import Constants



# Define the minimum and maximum coordinates for the billiard balls
X_MIN = 60
X_MAX = 1150
Y_MIN = 25
Y_MAX = 570
ERROR = 10

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

class BallConvertor:	
    
    def __init__(self, ppm, x_offset, y_offset):
        self.ppm = ppm
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.tilt_x = -11
        self.tilt_y = -4
        # blue is stripes
        self.stripe = list(range(1, 8))
        # green is solids
        self.solid = list(range(9, 16))
    
        
    
    def convertBall(self, cvBall : Ball):
        
        (pixel_pos_x, pixel_pos_y) = self.tilt_control(cvBall.x, cvBall.y)
        
        pos = self.convertPixelToFeet (pixel_pos_x, pixel_pos_y)

        if cvBall.color == BallColor.WHITE:
            return aiCueBall(pos)
        
        if cvBall.color == BallColor.BLUE:
            return aiBall(pos, self.stripe.pop())
        
        if cvBall.color == BallColor.GREEN:
            return aiBall(pos, self.solid.pop())
        
        if cvBall.color == BallColor.BLACK:
            return aiBall(pos, 8)   
        
    def convertPixelToFeet(self, x, y):
        
        x_feet = x / self.ppm
        y_feet = y / self.ppm
        
        x_feet += self.x_offset
        y_feet += self.y_offset
                
        return (x_feet, y_feet)
    
    def tilt_control(self, x_pixels, y_pixels):
        
        ratio_h = y_pixels / Constants.HEIGHT 
        ratio_w = x_pixels / Constants.WIDTH
        
        x_pixels += (ratio_w * self.tilt_x)
        y_pixels += (ratio_h * self.tilt_y)
        
        return (x_pixels, y_pixels)