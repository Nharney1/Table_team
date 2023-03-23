def DetermineNextSpeaker(currentPosition, targertPosition):
	convertedCurrentPosition = ConvertSpeakerToInternal(currentPosition)
	convertedTargertPosition = ConvertSpeakerToInternal(targertPosition)

	speakerList = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
	cornerList = [-1, 1, 5, 7]

	index = speakerList.index(convertedCurrentPosition)

	if convertedTargertPosition > convertedCurrentPosition: # Clockwise movement
		while True:
			index += 1
			if speakerList[index] == convertedTargertPosition or speakerList[index] in cornerList:
				return ConvertSpeakerToExternal(speakerList[index])
	elif convertedTargertPosition < convertedCurrentPosition: # Counterclockwise movement
		while True:
			index -= 1
			if speakerList[index] == convertedTargertPosition or speakerList[index] in cornerList:
				return ConvertSpeakerToExternal(speakerList[index])
	else:
		return ConvertSpeakerToExternal(speakerList[index])

def ConvertSpeakerToInternal(index):
	if index > 8:
		return index - 12
	else:
		return index

def ConvertSpeakerToExternal(index):
	if index <= 0:
		return index + 12
	else:
		return index
