import sys
import cv2 as cv 
import numpy as np

# Define the minimum and maximum coordinates for the billiard balls
X_MIN = 60
X_MAX = 1160
Y_MIN = 70
Y_MAX = 610

def DetectCircles():
	# Read in the input image
	path = '/home/table_team/Desktop/testing/test_images/input_02.png' # This will need to change, current image is a sample image
	img = cv.imread(path, cv.IMREAD_COLOR)

	# Resize the image, needed for displaying the output image
	width = int(img.shape[1] * 2)
	height = int(img.shape[0] * 2)
	dim = (width, height)
	resize_img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

	cv.imshow('balls', resize_img) # Testing only
	cv.waitKey(0)
	# Defined as:			y 		x
	resize_img = resize_img[50:720, 0:1200]
	cv.circle(resize_img, (60,70), 5, (255,0,0,), 5)
	cv.circle(resize_img, (1160,610), 5, (255,0,0,), 5)
	cv.imshow('balls', resize_img) # Testing only
	cv.waitKey(0)

	# Convert to grayscale for the Hough Circle Transform
	gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
	rows = gray_img.shape[0]

	# param1 sets sensitivity (how strong edges need to be). Higher values only pick up detailed edges
	# param2 sets how many edge points are needed. Lower finds more circle
	# param1, param2 = 36,22 seems to be the best values for accuracy
	circles = cv.HoughCircles(gray_img, cv.HOUGH_GRADIENT, 1, rows/8, param1 = 36, param2 = 21, minRadius = 15, maxRadius = 25)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			#			x     y
			center = (i[0], i[1])
			x = i[0]
			y = i[1]
			radius = i[2]
			arr = resize_img[y, x]
			if x < X_MIN or x > X_MAX or y < Y_MIN or y > Y_MAX:
				continue
			cv.circle(resize_img, center, radius, (255,0,255), 3)
			print(radius)
			print(center)
			print(arr)
			print('\n')
			cv.imshow('balls', resize_img)
			cv.waitKey(0)