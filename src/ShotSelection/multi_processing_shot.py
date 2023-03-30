from functools import partial
import math
from multiprocessing import Pool, cpu_count
import multiprocessing as mp
import pool_objets
import shot_verifier
import pool
from constants import Constants, Weights

board = None

def distance_to_closest_pocket(ball : pool_objets.Ball):
        closest = 999.0
        for pocket in pool.Pool.WORLD.pockets:
            x2 = ball.position[0] - pocket.x
            y2 = ball.position[1] - pocket.y
            dist = x2 * x2 + y2 * y2
            if dist < closest:
                closest = dist
        return math.sqrt(closest)

def compute_heuristic(board: pool_objets.PoolBoard, player : pool_objets.PoolPlayer) -> float:

        state = board.get_state()
        
        if state == pool_objets.PoolState.PLAYER1_WIN:
            return 1000.0
        elif state == pool_objets.PoolState.PLAYER2_WIN:
            return -1000.0
        pocketed_1 = board.player1_pocketed - board.previous_board.player1_pocketed
        pocketed_2 = board.player2_pocketed - board.previous_board.player2_pocketed

        heuristic = 0
        
        if player == pool_objets.PoolPlayer.PLAYER1:
            heuristic += pow(pocketed_1, 0.95) * Weights.POCKETED 
            heuristic -= pow(pocketed_2, 2) * Weights.POCKETED
        else:
            heuristic -= pow(pocketed_1, 2) * Weights.POCKETED 
            heuristic += pow(pocketed_1, 0.95) * Weights.POCKETED

        if board.turn == pool_objets.PoolPlayer.PLAYER1:
            heuristic += Weights.POSSESION
        else:
            heuristic -= Weights.POSSESION

        for ball in board.balls:
            if ball.number == 8:
                if board.player1_pocketed == 7:
                    dist = distance_to_closest_pocket(ball)
                    value = 1 / dist
                    heuristic += value
                if board.player2_pocketed == 7:
                    dist = distance_to_closest_pocket(ball)
                    value = 1 / dist
                    heuristic -= value
            else:
                dist = distance_to_closest_pocket(ball)
                value = min(1 / dist, 1.0)
                if ball.number < 8:
                    heuristic += value
                else:
                    heuristic -= value

        return heuristic

    

def compute_shot_heuristic(shot : pool_objets.Shot, original_board : pool_objets.PoolBoard) -> pool_objets.ComparableShot:

        pool.Pool.WORLD.load_board(original_board)
        pool.Pool.WORLD.shoot(shot)
        pool.Pool.WORLD.simulate_until_still(Constants.TIME_STEP, Constants.VEL_ITERS, Constants.POS_ITERS)
        current_board =  pool.Pool.WORLD.get_board_state()
        complexity =  pool.Pool.WORLD.complexity
        simplicity_heuristic = complexity.compute_complexity_heuristic(original_board.first_hit, current_board)
        heuristic = compute_heuristic(current_board, original_board.turn)
        
        if original_board.turn == pool_objets.PoolPlayer.PLAYER1:
            heuristic += (simplicity_heuristic)
            # calc scratches
            if current_board.cue_ball.pocketed:
                heuristic -= Weights.POCKET_CUE_BALL
            if original_board.first_hit == None:
                heuristic -= Weights.SCRATCH
            elif original_board.first_hit.number > 7:
                heuristic -= Weights.SCRATCH_OPPONENT_BALL
            
        else:
            heuristic -= (simplicity_heuristic)
            # calc scratches
            if current_board.cue_ball.pocketed:
                heuristic += Weights.POCKET_CUE_BALL        
            if original_board.first_hit == None:
                heuristic += Weights.SCRATCH
            elif original_board.first_hit.number < 9:
                heuristic += Weights.SCRATCH_OPPONENT_BALL
            
                
        if original_board.turn == pool_objets.PoolPlayer.PLAYER2:
            heuristic *= -1.0

        return (heuristic, shot.angle, shot.magnitude)

   
def getShot(shot, position, shortCircuit : mp.Event):
        magnitude, angle = shot
        shot = pool_objets.Shot(angle, magnitude, position)  
        if shot_verifier.verifyShotReachable(shot, board.balls):
            output = compute_shot_heuristic(shot=shot, original_board=board)
            return output
def worker(i, shortCircuit, position, listOfShots, output_list, start_index, end_index):

    for index in range(start_index, end_index):
        if not shortCircuit.is_set():
                shot = listOfShots[index]
                output = getShot(shot, position, shortCircuit)
                if output is not None:
                    if output[0] >= 35:
                        shortCircuit.set()
                    output_list.append(output)
    
            
        
def run(listOfShots, position):
    print("number of cores: " + str(cpu_count()))

    with mp.Manager() as manager:
        shortCircuit = mp.Event()
        outputList = manager.list()
        inputList = manager.list(listOfShots)
        processes = []
        lenInput = len(inputList)
        numProc = mp.cpu_count()
        offset = lenInput // numProc
        for i in range(mp.cpu_count()):
            start_index = offset * i
            end_index = (offset * (i + 1)) - 1
            p = mp.Process(target=worker, args=(i, shortCircuit, (position.x, position.y), inputList, outputList, start_index, end_index))
            p.start()
            processes.append(p)
            
        for p in processes:
            p.join()
        
        
        return list(outputList)