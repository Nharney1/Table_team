class Constants:
 
    # 28.575 MM POOL BALL RADIUS
    # 76 and 43 incg
    # 1930.4 and 1092.2
    TICK_RATE = 60
    SLOW_MOTION_TICK_RATE = 5
    PLAYER_WIDTH = 1.5
    TIME_STEP = 1.0 / TICK_RATE
    STICK_LENGTH = 57 / 12
    STICK_WIDTH = 1 / 12
    VEL_ITERS = 10
    POS_ITERS = 5
    TABLE_WIDTH = 76 / 12
    TABLE_HEIGHT = 43 / 12
    TABLE_RATIO = TABLE_WIDTH / TABLE_HEIGHT
    BALL_RADIUS =  0.1095
    POCKET_RADIUS = 2 / 12
    POCKET_WALL_OFFSET = 2.5 / 12
    WALL_THICKNESS = 5 / 12
    HEIGHT = 705   
    WIDTH = TABLE_RATIO * HEIGHT
    CUE_BALL = 0
    MAX_REACH = 3.5


class Weights:
    TOTAL_COLLISIONS = 0.98
    COLLISIONS_WITH_TABLE = 20
    POCKETED_BALL_COLLISIONS = 4
    TOTAL_DISTANCE = 1
    DISTANCE_BEFORE_CONTACT = 1.6
    POSSESION = 50
    POCKETED = 4
    POCKETED_WALL_COLLISIONS = 10
    DISTANCE_PER_BALL = 0.85
    SCRATCH = 30
    SCRATCH_OPPONENT_BALL = 50
    POCKET_CUE_BALL = 100
    GREAT_SHOT = 5
    GOOD_SHOT = 5
    WALL_EXPONENT = 2.7
    

class Bias:
    TOTAL_COLLISIONS = 1
    COLLISIONS_WITH_TABLE = 3
    POCKETED_BALL_COLLISIONS = 0

class BallColor:
    BILLIARD_GREEN = 39, 107, 64
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    WHITE = 255, 255, 255
    BROWN = 50, 28, 32
    YELLOW = 255, 215, 0
    BLUE = 0, 0, 255
    PURPLE = 128, 0, 128
    GREEN = 0, 128, 0
    BURGUNDY = 128, 0, 32
    ORANGE = 255, 165, 0
