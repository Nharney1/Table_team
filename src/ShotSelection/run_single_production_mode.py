import threading
import sys
from os.path import dirname

from src.ComputedShot import ComputedShot


pydir = dirname(__file__)
if pydir not in sys.path:
    sys.path.append(pydir)
    
from constants import Constants
from pool import Pool
import ai
from pool_objets import Ball, CueBall, PoolPlayer, Shot, PoolState
# Do not change order of import, ai must be imported before pool
import shot_verifier


# production mode means that there are no graphics
# single means that only one simulatation will be made

def runSingleProductionMode(balls, cueBall : CueBall, magnitudes, angles, pool_sim: Pool, turn: PoolPlayer = None):
        
        player1 = ai.RealisticAI(turn, magnitudes, angles)
        shot_queue = []
        finalShot = Shot(0,0)

        board = pool_sim.generate_board_from_list(balls, cueBall)
        if turn is not None: board.turn = turn
        Pool.WORLD.load_board(board)
        Pool.WORLD.board.turn_number = 2

        player1.take_shot(board, shot_queue)

        shot, time = shot_queue.pop()
        finalShot : Shot = shot
        
        angle = (finalShot.angle + 180) % 360
        angle *= -1
        
        body_pos = shot_verifier.getPlayerPosition(cueBall.position, angle)
        relative_angle = shot_verifier.getRelativeAngle(angle=angle, 
                                                        body_pos_x=body_pos[0],
                                                        body_pos_y=body_pos[1]
                                                        )
        wallNumber = shot_verifier.getWallNum(
            body_pos_x=body_pos[0],
            body_pos_y=body_pos[1]
        )
        force = finalShot.magnitude

        Pool.WORLD.board.shot = shot.angle
        Pool.WORLD.board.shot_ready = True

        pool_sim.WORLD.load_board(board)
        pool_sim.WORLD.shoot(shot)                
    
        computedShot : ComputedShot = ComputedShot(
            playerPos = body_pos,
            wallNumber = wallNumber,
            relativeAngle = relative_angle,
            force=force
        )

        print("Done!")   
        print(body_pos)
        print(relative_angle)
 
        return computedShot


if __name__ == "__main__":
    ##########################################
    ##This must be updated to pass in values##

    ballsProd = [
        Ball([2, 2], 1),
        Ball([3, 1.8], 8),
        Ball([4.8, 2.4], 9),  
        Ball([2.7, 0.5], 11),      
    ]
    cueBallProd = CueBall([2.5, 2.5])
 
    # Player 1 is solids and Player 2 is stripes
    playerTurn = PoolPlayer.PLAYER1
    ##########################################

    pool = Pool(slowMotion=False, graphics=False)
    magnitudes=[5, 8, 10, 12, 15]

    angles=range(0, 360, 1)
    runSingleProductionMode(ballsProd, cueBallProd, magnitudes, angles, pool, playerTurn)
    