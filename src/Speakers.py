x_min = 0
x_max = 6.33333
y_min = 0
y_max = 3.58333
offset = .2

def DetermineNextSpeaker(current, target):
	# Clockwise movement of corners
	cornerList = [11, 1, 5, 7]

	bottomLeftList = [9, 10, 11]	# Subsection 0
	leftList = [1, 11, 12]			# Subsection 1
	topList = [1, 2, 3, 4, 5]		# Subsection 2
	rightList = [5, 6, 7]			# Subsection 3
	bottomRightList = [7,8]			# Subsection 4
	
	targetList = []
	retlist = []

	currentSection = -1
	targetSection = -1

	# Returns the speakers to play if we are in the correct speaker subsection
	if set(target).issubset(topList):
		targetList = topList
	elif set(target).issubset(rightList):
		targetList = rightList
	elif set(target).issubset(bottomLeftList):
		targetList = bottomLeftList
	elif set(target).issubset(bottomRightList):
		targetList = bottomRightList
	elif set(target).issubset(leftList):
		targetList = leftList

	if set(current).issubset(targetList):
		return target

	# We are not in the correct speaker subsection
	# Get current section
	if set(current).issubset(bottomLeftList):
		currentSection = 0
	elif set(current).issubset(leftList):
		currentSection = 1
	elif set(current).issubset(topList):
		currentSection = 2
	elif set(current).issubset(rightList):
		currentSection = 3
	elif set(current).issubset(bottomRightList):
		currentSection = 4

	# Get target section
	if set(target).issubset(bottomLeftList):
		targetSection = 0
	elif set(target).issubset(leftList):
		targetSection = 1
	elif set(target).issubset(topList):
		targetSection = 2
	elif set(target).issubset(rightList):
		targetSection = 3
	elif set(target).issubset(bottomRightList):
		targetSection = 4

	if currentSection < targetSection:
		retlist.append(cornerList[currentSection])
	else:
		retlist.append(cornerList[currentSection - 1])
	return retlist


def ConvertSSToSpeaker(x, y):
	# Round to 2 decimal points
	x  = float(str(round(x,2)))
	y = float(str(round(y,2)))
	speakers = []

	# Shots were the user has to stand exactly in the corner are rare
	if x >= x_min and x <= x_min + offset and y >= y_min and y <= y_min + offset:
		speakers.append(1)
	elif x >= x_max - offset and x <= x_max and y >= y_min and y <= y_min + offset:
		speakers.append(5)
	elif x >= x_max - offset and x <= x_max and y >= y_max - offset and y <= y_max:
		speakers.append(7)
	elif x >= x_min and x <= x_min + offset and y >= y_max - offset and y <= y_max:
		speakers.append(11)

	if len(speakers) == 1:
		return speakers

	# If execution reaches here, the shot is not a corner shot
	if y <= y_min + offset:
		if x <= 1.2:
			speakers.extend([1,2])
			return speakers
		elif x <= 2:
			speakers.append(2)
			return speakers
		elif x <= 2.8:
			speakers.extend([2,3])
			return speakers
		elif x <= 3.5:
			speakers.append(3)
			return speakers
		elif x <= 4.3:
			speakers.extend([3,4])
			return speakers
		elif x <= 5.1:
			speakers.append(4)
			return speakers
		elif x <= x_max:
			speakers.extend([4,5])
			return speakers
	elif y >= y_max - offset:
		if x <= 1.2:
			speakers.extend([10,11])
			return speakers
		elif x <= 2:
			speakers.append(10)
			return speakers
		elif x <= 2.8:
			speakers.extend([9,10])
			return speakers
		elif x <= 3.5:
			speakers.append(9)
			return speakers
		elif x <= 4.3:
			speakers.extend([8,9])
			return speakers
		elif x <= 5.1:
			speakers.append(8)
			return speakers
		elif x <= x_max:
			speakers.extend([7,8])
			return speakers
	elif x <= x_min + offset:
		if y <= 1.35:
			speakers.extend([1,12])
			return speakers
		elif y <= 2.25:
			speakers.append(12)
			return speakers
		elif y <= y_max:
			speakers.extend([11,12])
			return speakers
	elif x >= x_max - offset:
		if y <= 1.35:
			speakers.extend([5,6])
			return speakers
		elif y <= 2.25:
			speakers.append(6)
			return speakers
		elif y <= y_max:
			speakers.extend([6,7])
			return speakers

	return speakers

def UserArrived(currentList, targetList):
	if len(currentList) == 1:
		if currentList[0] in targetList:
			return True
	elif len(currentList) == 2:
		if currentList[0] in targetList or currentList[1] in targetList:
			return True
		return False

# Tests
if __name__ == '__main__':

	print(UserArrived([1,2], [2,3]))
	print(UserArrived([1,2], [4,5]))
	print(UserArrived([1,2], [2,1]))
	print(UserArrived([5,6], [6,5]))


	print(DetermineNextSpeaker([1,2],[1]))
	print(DetermineNextSpeaker([1,2],[2]))
	print(DetermineNextSpeaker([1,2],[3,4]))
	print(DetermineNextSpeaker([1,2],[4]))
	print(DetermineNextSpeaker([1,2],[5]))

	print(DetermineNextSpeaker([10],[10,11]))
	print(DetermineNextSpeaker([9],[11]))
	print(DetermineNextSpeaker([7],[7,8]))

	print(DetermineNextSpeaker([10],[4,5]))
	print(DetermineNextSpeaker([4,5],[10]))
	print(DetermineNextSpeaker([11,12],[10,11]))
	print(DetermineNextSpeaker([10,11],[11]))
	print(DetermineNextSpeaker([7,8],[7]))
	print(DetermineNextSpeaker([1,2],[3,4]))
	print(DetermineNextSpeaker([3,4],[1,2]))
	print(DetermineNextSpeaker([6,7],[9]))
	print(DetermineNextSpeaker([1,12],[7,8]))
	print(DetermineNextSpeaker([7,8],[1,12]))
	print(DetermineNextSpeaker([8],[9]))


	# Corners
	print("Expected 1 got: " + str(ConvertSSToSpeaker(.1,0)))
	print("Expected 1 got: " + str(ConvertSSToSpeaker(.1,.1)))
	print("Expected 1 got: " + str(ConvertSSToSpeaker(0,.1)))
	print("Expected 5 got: " + str(ConvertSSToSpeaker(6.2,0)))
	print("Expected 5 got: " + str(ConvertSSToSpeaker(6.3,.1)))
	print("Expected 5 got: " + str(ConvertSSToSpeaker(6.2,.1)))
	print("Expected 7 got: " + str(ConvertSSToSpeaker(6.2,3.58)))
	print("Expected 7 got: " + str(ConvertSSToSpeaker(6.3,3.5)))
	print("Expected 7 got: " + str(ConvertSSToSpeaker(6.2,3.5)))
	print("Expected 11 got: " + str(ConvertSSToSpeaker(0,3.5)))
	print("Expected 11 got: " + str(ConvertSSToSpeaker(.1,3.58)))
	print("Expected 11 got: " + str(ConvertSSToSpeaker(.1,3.5)))

	# Top
	print("Expected 1 and 2 got: " + str(ConvertSSToSpeaker(.7, 0)))
	print("Expected 1 and 2 got: " + str(ConvertSSToSpeaker(.9, 0)))
	print("Expected 2 got: " + str(ConvertSSToSpeaker(1.9, 0)))
	print("Expected 2 and 3 got: " + str(ConvertSSToSpeaker(2.5,0)))
	print("Expected 3 got: " + str(ConvertSSToSpeaker(2.9,0)))
	print("Expected 3 and 4 got: " + str(ConvertSSToSpeaker(3.6,0)))
	print("Expected 4 got: " + str(ConvertSSToSpeaker(4.4,0)))
	print("Expected 4 and 5 got: " + str(ConvertSSToSpeaker(5.2,0)))
	print("Expected 4 and 5 got: " + str(ConvertSSToSpeaker(6.1,0)))

	# Bottom
	print("Expected 10 and 11 got: " + str(ConvertSSToSpeaker(.7,3.6)))
	print("Expected 10 and 11 got: " + str(ConvertSSToSpeaker(.9,3.6)))
	print("Expected 10 got: " + str(ConvertSSToSpeaker(1.9,3.6)))
	print("Expected 9 and 10 got: " + str(ConvertSSToSpeaker(2.5,3.6)))
	print("Expected 9 got: " + str(ConvertSSToSpeaker(2.9,3.6)))
	print("Expected 8 and 9 got: " + str(ConvertSSToSpeaker(3.6,3.6)))
	print("Expected 8 got: " + str(ConvertSSToSpeaker(4.4,3.6)))
	print("Expected 7 and 8 got: " + str(ConvertSSToSpeaker(5.2,3.6)))
	print("Expected 7 and 8 got: " + str(ConvertSSToSpeaker(6.1,3.6)))

	# Left
	print("Expected 1 and 12 got: " + str(ConvertSSToSpeaker(0,.8)))
	print("Expected 1 and 12 got: " + str(ConvertSSToSpeaker(0,1)))
	print("Expected 12 got: " + str(ConvertSSToSpeaker(0,1.5)))
	print("Expected 11 and 12 got: " + str(ConvertSSToSpeaker(0, 2.3)))
	print("Expected 11 and 12 got: " + str(ConvertSSToSpeaker(0,2.5)))

	# Right
	print("Expected 5 and 6 got: " + str(ConvertSSToSpeaker(6.3,.8)))
	print("Expected 5 and 6 got: " + str(ConvertSSToSpeaker(6.3,1)))
	print("Expected 6 got: " + str(ConvertSSToSpeaker(6.3,1.5)))
	print("Expected 6 and 7 got: " + str(ConvertSSToSpeaker(6.3,2.3)))
	print("Expected 6 and 7 got: " + str(ConvertSSToSpeaker(6.3,2.5)))
