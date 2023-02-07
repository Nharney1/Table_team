class InvalidBallCount(Exception):
	pass

def DetectShot(previousShot, currentShot):
	p_black = 0
	p_white = 0
	p_green = 0
	p_blue = 0

	for ball in previousShot:
		if ball.color == 'black':
			p_black += 1
		if ball.color == 'white':
			p_white += 1
		if ball.color == 'green':
			p_green += 1
		if ball.color == 'blue':
			p_blue += 1

	c_black = 0
	c_white = 0
	c_green = 0
	c_blue = 0

	for ball in currentShot:
		if ball.color == 'black':
			c_black += 1
		if ball.color == 'white':
			c_white += 1
		if ball.color == 'green':
			c_green += 1
		if ball.color == 'blue':
			c_blue += 1

	if p_black > 1 or p_white > 1 or c_black > 1 or c_white > 1:
		raise InvalidBallCount

	# Assume the user is using the blue balls
	# Check if the user made a game ball or opponent ball
	if c_blue < p_blue:
		for i in range (p_blue - c_blue):
			print("Game ball made!")
	if c_green < p_green:
		for i in range (p_green - c_green):
			print("Opponent ball made!")

	# Check if there is an end game scenario
	if c_black == 0 and c_white == 0:
		print("Sunk black and white ball")
		return 'loss'
	elif c_black == 0 and c_blue > 0:
		print("Sunk black ball before all game balls were sunk")
		return 'loss'
	elif c_black == 0 and c_white == 1 and c_blue == 0:
		print("Sunk the black ball, winner!")
		return 'win'
	elif c_black == 1 and c_white == 0:
		print("Scratch: sunk the white ball")
		return 'continue'
	else:
		return 'continue'
