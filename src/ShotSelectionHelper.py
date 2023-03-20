from src.ComputedShot import ComputedShot
from src.ShotSelection.run_single_test_mode import runSingleTestMode
from src.ShotSelection.pool import Pool
from src.ShotSelection.pool_objets import PoolPlayer, CueBall as aiCueBall, Ball as aiBall
from src.ShotSelection.constants import Constants
 
# importing
from src import Ball as cvBall
from src.Ball import BallColor as cvBallColor
        			
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
    
        
    
    def convertBall(self, cvBall : cvBall):
        
        (pixel_pos_x, pixel_pos_y) = self.tilt_control(cvBall.x, cvBall.y)
        
        pos = self.convertPixelToFeet (pixel_pos_x, pixel_pos_y)

        if cvBall.color == cvBallColor.WHITE:
            return aiCueBall(pos)
        
        if cvBall.color == cvBallColor.BLUE:
            return aiBall(pos, self.stripe.pop())
        
        if cvBall.color == cvBallColor.GREEN:
            return aiBall(pos, self.solid.pop())
        
        if cvBall.color == cvBallColor.BLACK:
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
    
    
def computeShot(Current_Ball_List): 
    # Player 1 is solids and Player 2 is stripes
    playerTurn = PoolPlayer.PLAYER1
    pool = Pool(slowMotion=False, graphics=True)
    magnitudes = [5, 10, 15, 20, 25]
    angles = range(0, 360, 1)

    ballsProd = list()
            
    ppf = 195
    
    x_offset = Constants.WALL_THICKNESS
    y_offset = Constants.WALL_THICKNESS
    
    
    convertor = BallConvertor(ppf, x_offset, y_offset)
    
    cueBallProd = aiCueBall((0,0))
    
    for ball in Current_Ball_List:
        convertedBall = convertor.convertBall(ball)
        if convertedBall is not None:
            if convertedBall.number == 0:
                cueBallProd = convertedBall
            else:
                ballsProd.append(convertedBall)
    
    
    computedShot : ComputedShot = runSingleTestMode(
        balls=ballsProd, 
        cueBall=cueBallProd, 
        magnitudes=magnitudes, 
        angles=angles, 
        pool_sim=pool, 
        turn=playerTurn
    )
    print("force: {0}, relative angle: {1}".format(computedShot.force, computedShot.relativeAngle))
    print("Player pos x: {0}, Player pos y: {1}, Wall Number: {2}".format(
        computedShot.playerPos[0], computedShot.playerPos[1], computedShot.wallNumber
    ))
    
    return computedShot
        
