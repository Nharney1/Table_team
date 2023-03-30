import os
from typing import List
import cv2 as cv 
import numpy as np
from .Ball import (Ball,
				   X_MAX,
				   Y_MAX,
				   X_MIN,
				   Y_MIN,
				   ERROR)

SHOW_IMAGES = True

def DetectCircles() -> List[Ball]:
	Ball_list = []

	dirname = os.path.dirname(__file__)

	path = os.path.join(dirname, 'test_images/input_25.png')
	#path = '/home/table_team/input.png'
	img = cv.imread(path, cv.IMREAD_COLOR)

	# Resize the image, needed for displaying the output image
	width = int(img.shape[1] * 2)
	height = int(img.shape[0] * 2)
	dim = (width, height)
	resize_img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

	# Crop the image [y:x]
	resize_img = resize_img[60:680, 40:1240]

	if SHOW_IMAGES:
		# Show the minimum and maximum location for balls (corners of table)
		cv.circle(resize_img, (X_MIN, Y_MIN), 5, (255,0,0,), 5)
		cv.circle(resize_img, (X_MAX,Y_MAX), 5, (255,0,0,), 5) 
		#cv.imshow('balls', resize_img) 
		cv.waitKey(0)
		#cv.destroyAllWindows()

	# Convert to grayscale for the Hough Circle Transform
	gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)

	dp = 1
	min_distance = 40
	
	# Make the call to detect circles in image
	circles = cv.HoughCircles(gray_img, cv.HOUGH_GRADIENT, dp, min_distance, param1 = 30, param2 = 14, minRadius = 15, maxRadius = 25)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:

			# Extract information from contours
			x = i[0]
			y = i[1]
			center = (i[0], i[1])
			radius = i[2]

			# Skip over any noise in the corners
			if x < X_MIN + ERROR or x > X_MAX - ERROR or y < Y_MIN + ERROR or y > Y_MAX - ERROR:
				continue

			# Draw a circle around the ball
			cv.circle(resize_img, center, radius, (255,255,255), 3)

			# Determine the color of the ball
			temp_ball = Ball(x,y,radius)
			temp_ball.CleanBGRVector(resize_img)
			temp_ball.SetColor()
			Ball_list.append(temp_ball)

			#if SHOW_IMAGES: 
				#cv.imshow('balls', resize_img)
				#cv.waitKey(0)

		cv.destroyAllWindows()

		return Ball_list
