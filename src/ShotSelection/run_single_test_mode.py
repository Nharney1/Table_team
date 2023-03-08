import threading
import sys
from os.path import dirname

pydir = dirname(__file__)
if pydir not in sys.path:
    sys.path.append(pydir)
    
from constants import Constants    
import ai
from pool import Pool
from pool_objets import CueBall, Ball, PoolPlayer, PoolState, Shot
import shot_verifier
import pygame.display
import pygame.draw
import pygame.event
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, VIDEORESIZE)
import pygame.time

def runSingleTestMode(balls, cueBall, magnitudes, angles, pool_sim: Pool, turn: PoolPlayer = None):
        
        player1 = ai.RealisticAI(PoolPlayer.PLAYER1, magnitudes, angles)
        shot_queue = []
        ai_thinking = False
        simulating = False
        fast_forward = True
        finalShot = Shot(0,0)

        board = pool_sim.generate_board_from_list(balls, cueBall)
        board.previous_board = board
        if turn is not None: board.turn = turn
        Pool.WORLD.load_board(board)
        Pool.WORLD.board.turn_number = 2
        
        graphics = Pool.WORLD.get_graphics()
        shots = 0

        still_frames = 0
        # game loop
        while shots < 2:
            # Check the event queue
            for event in pygame.event.get():
            
                if event.type == VIDEORESIZE:
                    pool_sim.screen.screen_height = event.h
                    pool_sim.screen.screen_width = event.w
                    pool_sim.update_screen()
                    pool_sim.screen.screen = pygame.display.set_mode((pool_sim.screen.screen_width, pool_sim.screen.screen_height), RESIZABLE)
            
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
                
                body_pos = shot_verifier.getPlayerPosition(cueBall.position, angle)
                relative_angle = shot_verifier.getRelativeAngle(angle=angle, 
                                                                body_pos_x=body_pos[0],
                                                                body_pos_y=body_pos[1]
                                                                )
                
                Pool.WORLD.board.shot = shot.angle
                Pool.WORLD.board.shot_ready = True
                pool_sim.update_graphics(graphics)
                pygame.time.delay(4000)
                Pool.WORLD.load_board(board)
                Pool.WORLD.shoot(shot)                
            
            if simulating:
                for _ in range(3 if fast_forward else 1):
                    if not Pool.WORLD.update_physics(Constants.TIME_STEP, Constants.VEL_ITERS, Constants.POS_ITERS):
                        still_frames += 1
                    else:
                        still_frames = 0
                graphics = Pool.WORLD.get_graphics()
                if still_frames > 3:
                    board = Pool.WORLD.get_board_state()
                    state = board.get_state()
                    
                    if state == PoolState.ONGOING:
                        simulating = False
                    else:
                        board = pool.generate_normal_board()
                        simulating = False
                        
                    Pool.WORLD.load_board(board)
                    graphics = Pool.WORLD.get_graphics()
                    
            pool_sim.update_graphics(graphics)
            
        print("Done!")   
        print(body_pos)
        print(relative_angle)



if __name__ == "__main__":
    ##########################################
    ##This must be updated to pass in values##

    balls_test_1 = [
        Ball([0, 0], 8),
        Ball([6, 3.7], 3),  
        Ball([4.0, 2.15], 4)     
    ]
    cueBall_test_1 = CueBall([1, 1])
    
    balls_test_2 = [
        Ball([3, 3], 8),
        Ball([6, 4], 3),  
        Ball([4.4, 2.15], 4)     
    ]
    cueBall_test_2 = CueBall([1, 1])
    
    balls_test_3 = [
        Ball([3, 3], 8),
        Ball([2, 3.3], 3),  
        Ball([3.8, 1], 4)     
    ]
    cueBall_test_3 = CueBall([2, 2])
    
    balls_test_4 = [
        Ball([3, 3], 8),
        Ball([3.3, 1], 3),  
        Ball([1.5, 3.8], 4)     
    ]
    cueBall_test_4 = CueBall([1, 2.5])
    
    balls_test_5 = [
        Ball([2, 1], 8),
        Ball([5, 1.3], 3),  
        Ball([2, 3], 4)     
    ]
    cueBall_test_5 = CueBall([1, 2.5])
    
    balls_test_6 = [
        Ball([5.2, 3], 8),
        Ball([6, 1.8], 3),  
        Ball([1, 3], 4)     
    ]
    cueBall_test_6 = CueBall([1, 2.5])
    
    test_cases = [(cueBall_test_1, balls_test_1), (cueBall_test_4, balls_test_4), (cueBall_test_6, balls_test_6),
        (cueBall_test_5, balls_test_5), 
        (cueBall_test_2, balls_test_2), (cueBall_test_3, balls_test_3)]
    
    # Player 1 is solids and Player 2 is stripes
    playerTurn = PoolPlayer.PLAYER1
    ##########################################

    pool = Pool(slowMotion=False, graphics=True)
    magnitudes=[45, 75, 90]
    angles=range(0, 360, 1)
    
    ballsProd = [
        Ball([2, 2], 1),
        Ball([3, 1.8], 8),
        Ball([4.8, 2.4], 9),  
        Ball([2.7, 0.5], 11),      
    ]
    cueBallProd = CueBall([2.5, 2.5])
 
    runSingleTestMode(ballsProd, cueBallProd, magnitudes, angles, pool, playerTurn)
    # for cueBall, balls in test_cases:
    #     runSingleTestMode(balls, cueBall, magnitudes, angles, pool, playerTurn)
    