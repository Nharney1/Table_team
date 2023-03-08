import threading

import sys
from os.path import dirname

pydir = dirname(__file__)
if pydir not in sys.path:
    sys.path.append(pydir)
    
from constants import Constants
from pool import Pool
import ai
from pool_objets import Ball, CueBall, PoolPlayer, Shot, PoolState
# Do not change order of import, ai must be imported before pool
from shot_verifier import getRelativeAngle, getPlayerPosition


# production mode means that there are no graphics
# single means that only one simulatation will be made

def runSingleProductionMode(balls, cueBall : CueBall, magnitudes, angles, pool_sim: Pool, turn: PoolPlayer):
        
        player1 = ai.RealisticAI(turn, magnitudes, angles)
        shot_queue = []
        ai_thinking = False
        simulating = False
        fast_forward = True
        finalShot = Shot(0,0)

        board = pool_sim.generate_board_from_list(balls, cueBall)
        if turn is not None: board.turn = turn
        Pool.WORLD.load_board(board)
        Pool.WORLD.board.turn_number = 2

        shots = 0
        still_frames = 0
        # game loop
        while shots < 2:
       
            if not simulating and not ai_thinking and len(shot_queue) == 0:
                target = player1.take_shot
                if shots < 1:
                    threading.Thread(target=target, args=(board, shot_queue)).start()
                shots += 1
                ai_thinking = True
            elif len(shot_queue) > 0:
                ai_thinking = False
                simulating = True
                shot, time = shot_queue.pop()
                finalShot, finalTime = shot, time
                
                
                angle = (finalShot.angle + 180) % 360
                angle *= -1
                
                body_pos = getPlayerPosition(cueBall.position, angle)
                relative_angle = getRelativeAngle(angle=angle, 
                                                                body_pos_x=body_pos[0],
                                                                body_pos_y=body_pos[1]
                                                                )
                
                pool_sim.WORLD.load_board(board)
                pool_sim.WORLD.shoot(shot)                
            
            if simulating:
                for _ in range(5 if fast_forward else 1):
                    if not Pool.WORLD.update_physics(Constants.TIME_STEP, Constants.VEL_ITERS, Constants.POS_ITERS):
                        still_frames += 1
                    else:
                        still_frames = 0
            
                if still_frames > 3:
                    board = Pool.WORLD.get_board_state()
                    state = board.get_state()
                    if state == PoolState.ONGOING:
                        simulating = False
                    else:
                        board = pool.generate_normal_board()
                        simulating = False
                    Pool.WORLD.load_board(board)
        print("Done!")   
        print(body_pos)
        print(relative_angle)
 


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
    magnitudes=[45, 75, 90]
    angles=range(0, 360, 1)
    runSingleProductionMode(ballsProd, cueBallProd, magnitudes, angles, pool, playerTurn)
    