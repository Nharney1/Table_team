from .Ball import BallColor

GAME_BALL_MADE = 200
OPPONENT_BALL_MADE = 201
BLACK_AND_WHITE = 202
BLACK_BEFORE_GAME_BALLS = 203
BLACK_BALL_WINNER  = 204
SCRATCH  = 205
NOTHING = 206

command_list  = []

class InvalidBallCount(Exception):
	pass

def DetermineShotOutcome(previousShot, currentShot):
	p_black = 0
	p_white = 0
	p_green = 0
	p_blue = 0

	for ball in previousShot:
		if ball.color == BallColor.BLACK:
			p_black += 1
			print("Got  black")
		if ball.color == BallColor.WHITE:
			p_white += 1
			print('Got  white')
		if ball.color == BallColor.GREEN:
			p_green += 1
			print('Got  green')
		if ball.color == BallColor.BLUE:
			p_blue += 1
			print("Got blue")

	c_black = 0
	c_white = 0
	c_green = 0
	c_blue = 0

	for ball in currentShot:
		if ball.color == BallColor.BLACK:
			c_black += 1
		if ball.color == BallColor.WHITE:
			c_white += 1
		if ball.color == BallColor.GREEN:
			c_green += 1
		if ball.color == BallColor.BLUE:
			c_blue += 1

	if p_black > 1 or p_white > 1 or c_black > 1 or c_white > 1:
		raise InvalidBallCount

	# Assume the user is using the blue balls
	# Check if the user made a game ball or opponent ball
	if c_blue < p_blue:
		for i in range (p_blue - c_blue):
			print("Game ball made!")
			command_list.append(GAME_BALL_MADE)
	if c_green < p_green:
		for i in range (p_green - c_green):
			print("Opponent ball made!")
			command_list.append(OPPONENT_BALL_MADE)

	# Check if there is an end game scenario
	if c_black == 0 and c_white == 0:
		print("Sunk black and white ball")
		command_list.append(BLACK_AND_WHITE)
	elif c_black == 0 and c_blue > 0:
		print("Sunk black ball before all game balls were sunk")
		command_list.append(BLACK_BEFORE_GAME_BALLS)
	elif c_black == 0 and c_white == 1 and c_blue == 0:
		print("Sunk the black ball, winner!")
		command_list.append(BLACK_BALL_WINNER)
	elif c_black == 1 and c_white == 0:
		print("Scratch: sunk the white ball")
		command_list.append(SCRATCH)

	return command_list