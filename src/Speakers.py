import math
from .ComputedShot import ComputedShot


x_min = 0
x_max = 6.33333
y_min = 0
y_max = 3.58333
offset = .2

def DetermineAngleSpeaker(current_speaker_list : list, computed_shot: ComputedShot):
	# Determine the the speaker(s) to play in order
	# to guide the user toward the relative_angle of their shot
	# current is the number of the current speaker you are on
	speaker_set = {
		1 : (0,0),
		2 : (x_max / 5, 0),
		3 : (x_max / 2, 0),
		4 : ((4 * x_max) / 5, 0),
		5 : (x_max, 0),
		6 : (x_max, y_max / 2),
		7 : (x_max, y_max),
		8 : ((4 * x_max) / 5, y_max),
		9 : (x_max / 2, y_max),
		10 : (x_max / 5, y_max),
		11 : (0, y_max),
		12 : (0, y_max / 2),
	}

	angles = {}
	player_x, player_y = computed_shot.playerPos
	current = None

	# Find which speaker is closer to the player
	if len(current_speaker_list) == 1:
		current = current_speaker_list[0]
	else:
		speaker_1 = current_speaker_list[0]
		speaker_2 = current_speaker_list[1]

		speaker_1_x, speaker_1_y = speaker_set[speaker_1]
		speaker_2_x, speaker_2_y = speaker_set[speaker_2]

		dist_1 = math.sqrt(math.pow(player_x - speaker_1_x, 2) + math.pow(player_y - speaker_1_y, 2))
		dist_2 = math.sqrt(math.pow(player_x - speaker_2_x, 2) + math.pow(player_y - speaker_2_y, 2))

		current = speaker_1 if dist_1 < dist_2 else speaker_2



	# edge cases with 0, 90, or -90 degrees

	straight_angle = None
	if abs(computed_shot.relativeAngle) < 5: straight_angle = 0
	if abs(computed_shot.relativeAngle - 90) < 5: straight_angle = 90
	if abs(computed_shot.relativeAngle + 90) < 5: straight_angle = -90

	if straight_angle is not None:
		if computed_shot.wallNumber == 1:
			if straight_angle == -90:
				return [7]
			elif straight_angle == 90:
				return[5]
			elif straight_angle == 0:
				if current == 7:
					return[11]
				elif current == 5:
					return [1]
		elif computed_shot.wallNumber == 2:
			if straight_angle == -90:
				return [5]
			elif straight_angle == 90:
				return[1]
			elif straight_angle == 0:
				if current == 1:
					return [11]
				elif current == 5:
					return [7]
		elif computed_shot.wallNumber == 3:
			if straight_angle == -90:
				return [1]
			elif straight_angle == 90:
				return[11]
			elif straight_angle == 0:
				if current == 1:
					return [5]
				elif current == 11:
					return [7]
		elif computed_shot.wallNumber == 4:
			if straight_angle == -90:
				return [11]
			elif straight_angle == 90:
				return[7]
			elif straight_angle == 0:
				if current == 11:
					return [1]
				elif current == 7:
					return [5]
		
		
	# Compute angle between player and pocket
	for speaker_num in range(1, 13):

		if current == speaker_num: continue

		angle = None
		speaker_x, speaker_y = speaker_set[speaker_num]

		if computed_shot.wallNumber == 2 or computed_shot.wallNumber == 4:

			opposite = -(speaker_y - player_y)
			adjacent = speaker_x - player_x

			if adjacent == 0:
				angle = 0
			elif opposite == 0:
				angle = None
				if adjacent > 0:
					angle = 90
				else:
					angle = -90
				if computed_shot.wallNumber == 2:
					angle *= -1
			else:
				angle = math.atan(opposite / adjacent)
				angle = math.degrees(angle)
				if angle < 0:
					angle = -90 - angle
				else:
					angle = 90 - angle
		else:
			opposite = speaker_x - player_x
			adjacent = -(speaker_y - player_y)

			if adjacent == 0:
				angle = 0
			elif opposite == 0:
				if adjacent > 0:
					angle = 90
				else:
					angle = -90
				if computed_shot.wallNumber == 3:
					angle *= -1
			else:
				angle = math.atan(opposite / adjacent)
				angle = math.degrees(angle)
				if angle < 0:
					angle = -90 - angle
				else:
					angle = 90 - angle
				angle *= -1

		angles[speaker_num] = angle
			
	# Find closest angle
	rounded_angle = round(computed_shot.relativeAngle, 1)
	lower_bound = None
	upper_bound = None

	for speaker_num in angles:
		speaker_angle = round(angles[speaker_num], 1)

		if abs(speaker_angle - rounded_angle) < 5:
			return [speaker_num]
		
		if speaker_angle < rounded_angle:
			if (lower_bound is None or
				(rounded_angle - speaker_angle) < (rounded_angle - angles[lower_bound])):
				lower_bound = speaker_num
		elif speaker_angle > rounded_angle:
			if (upper_bound is None or
				(speaker_angle - rounded_angle) < (angles[upper_bound] - rounded_angle)):
				upper_bound = speaker_num

	return [lower_bound, upper_bound]

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
	print("In UserArrived" + str(currentList))
	if len(currentList) == 0:
		return False
	elif len(targetList) == 1:
		if currentList[0] in targetList or currentList[1] in targetList:
			return True
	elif len(targetList) == 2:
		if currentList[0] in targetList and currentList[1] in targetList:
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

	# Angle tests
	shot = ComputedShot((x_max, y_max), -45, 4, 10)
	print("Expected speaker 3, got: " + str(DetermineAngleSpeaker([7], shot)))
	shot = ComputedShot((x_max / 2, 0), -45, 2, 10)
	print("Expected speaker 7, got: " + str(DetermineAngleSpeaker([3], shot)))
	shot = ComputedShot((x_max, y_max / 2), 8, 1, 10)
	print("Expected speaker 12 and 1, got: " + str(DetermineAngleSpeaker([6], shot)))
	shot = ComputedShot((0, y_max / 2), 8, 3, 10)
	print("Expected speaker 6 and 7, got: " + str(DetermineAngleSpeaker([12], shot)))
	shot = ComputedShot((x_max / 5, y_max), 0, 4, 10)
	print("Expected speaker 2, got: " + str(DetermineAngleSpeaker([10], shot)))
	shot = ComputedShot((4 * x_max / 5, 0), 0, 2, 10)
	print("Expected speaker 8, got: " + str(DetermineAngleSpeaker([4], shot)))
	shot = ComputedShot((4 * x_max / 5, 0), 10, 2, 10)
	print("Expected speaker 8 and 9, got: " + str(DetermineAngleSpeaker([4], shot)))
	shot = ComputedShot((x_max, y_max), 0, 1, 10)
	print("Expected speaker 11, got: " + str(DetermineAngleSpeaker([7], shot)))
	shot = ComputedShot((x_max, y_max), 0, 4, 10)
	print("Expected speaker 5, got: " + str(DetermineAngleSpeaker([7], shot)))
	shot = ComputedShot((x_max / 2, 0), 0, 2, 10)
	print("Expected speaker 9, got: " + str(DetermineAngleSpeaker([3], shot)))
	shot = ComputedShot((x_max / 2, 0), 0, 2, 10)
	print("Expected speaker 9, got: " + str(DetermineAngleSpeaker([3,4], shot)))




	 
