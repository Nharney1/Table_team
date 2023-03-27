ROW_TOP  = .25
ROW_BOTTOM = 3.25  # May need to adjust this
COL_1 = .25
COL_2 = 2.25
COL_3 = 4
COL_4 = 6

def ConvertSSToSpeaker(x, y):
	# Round to 2 decimal points
	x  = float(str(round(x,2)))
	y = float(str(round(y,2)))

	if y <= ROW_TOP:
		if x <= COL_1:
			return 1
		elif x <= COL_2:
			return 2
		elif  x <= COL_3:
			return 3
		elif x <= COL_4:
			return 4
		else:
			return  5
	elif y > ROW_TOP and y < ROW_BOTTOM:
		if x  <= COL_1:
			return 12
		else:
			return 6
	else:
		if x <= COL_1:
			return 11
		elif x <= COL_2:
			return 10
		elif  x <= COL_3:
			return 9
		elif x <= COL_4:
			return 8
		else:
			return  7
