from Box2D.Box2D import *
import pygame.display
import pygame.draw
import pygame.event
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, VIDEORESIZE)
import pygame.time
import random
import threading
import ai
from pool_objets import *
from constants import Constants
import drawable

class Pool:
    WORLD = PoolWorld()
    def __init__(self, slowMotion=False, graphics=True):
        self.slowMotion = slowMotion
        self.graphics = graphics

        if self.graphics:
            pygame.init()
            self.screen = drawable.ScreenInfo(pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT )), Constants.WIDTH, Constants.HEIGHT, 0, 0, 0)
            pygame.display.set_caption("Billiards")
            self.clock = pygame.time.Clock()

            self.update_screen()

    def update_screen(self):
        # update ppm
        if self.screen.screen_width / self.screen.screen_height <= Constants.TABLE_RATIO:
            self.screen.ppm = self.screen.screen_width / Constants.TABLE_WIDTH
        else:
            self.screen.ppm = self.screen.screen_height / Constants.TABLE_HEIGHT

        # update offsets
        ratio = self.screen.screen_width / self.screen.screen_height
        if ratio == Constants.TABLE_RATIO:
            self.screen.offset_x = 0
            self.screen.offset_y = 0
        elif ratio > Constants.TABLE_RATIO:
            self.screen.offset_x = int(self.screen.screen_width - (Constants.TABLE_RATIO * self.screen.screen_height)) // 2
            self.screen.offset_y = 0
        else:
            self.screen.offset_x = 0
            self.screen.offset_y = int((self.screen.screen_height - (self.screen.screen_width / Constants.TABLE_RATIO))) // 2

    def update_graphics(self, graphics:PoolGraphics):
        # Fill in background
        self.screen.screen.fill(BallColor.BILLIARD_GREEN)

        # Draw the separately pockets (because they don't actually exist)
        for pt in graphics.pockets:
            x = pt.x * self.screen.ppm
            y = pt.y * self.screen.ppm
            position = [x + self.screen.offset_x, self.screen.screen_height - y - self.screen.offset_y]
            pygame.draw.circle(self.screen.screen, BallColor.BLACK, position, Constants.POCKET_RADIUS * self.screen.ppm)

        # Draw drawables
        for drawable in graphics.drawables:
            drawable.draw(self.screen)
        
        drawable.draw_pool_cue(self.screen, graphics.board.cue_ball.position, graphics.board.shot, graphics.board.shot_ready)
        drawable.draw_player_pos(self.screen, graphics.board.cue_ball.position, graphics.board.shot, graphics.board.shot_ready, graphics.board.balls)
        # Draw the pocketed balls at the bottom of the screen
        for ball in graphics.pocketed_balls:
            r = Constants.BALL_RADIUS * self.screen.ppm
            h = self.screen.screen.get_height()
            y = h - (h - self.screen.screen_height) // 2
            x = (ball.number + 0.5) / 16 * self.screen.screen_width
            drawable.draw_billiard_ball_helper([x, y], r, self.screen, ball.color, BallColor.WHITE if 
                                                        ball.number != Constants.CUE_BALL else BallColor.BLACK, ball.number, 0)

        for ball in graphics.unpocketed_balls:
            r = Constants.BALL_RADIUS * self.screen.ppm
            x = ball.position[0] * self.screen.ppm
            y = ball.position[1] * self.screen.ppm
            drawable.draw_billiard_ball_helper([x, y], r, self.screen, ball.color, BallColor.WHITE if 
                                                        ball.number != Constants.CUE_BALL else BallColor.BLACK, ball.number, ball.angle)

        # Draw which players turn it is (blue bar if player 1, red bar if player 2)
        if graphics.board.get_state() == PoolState.ONGOING:
            width = self.screen.screen.get_width() // 2
            h = self.screen.screen.get_height()
            height = h // 96
            top = h - height
            if graphics.board.turn == PoolPlayer.PLAYER1:
                left = 0
                color = BallColor.BLUE
            else:
                left = width
                color = BallColor.RED
            pygame.draw.rect(self.screen.screen, color, [left, top, width, height])

        # Flip the screen and try to keep at the target FPS
        pygame.display.flip()
        self.clock.tick(Constants.TICK_RATE if not self.slowMotion else Constants.SLOW_MOTION_TICK_RATE)

    def generate_random_board(self) -> PoolBoard:
        balls = []
        for i in range(8):
            balls.append(Ball([random_float(0.5, Constants.TABLE_WIDTH - 0.5), random_float(0.5, Constants.TABLE_HEIGHT - 0.5)], i))
        
        return PoolBoard(CueBall([2.5, 2.5]), balls)
    
    def generate_board_from_list(self, ballsOnTable, cueBall) -> PoolBoard:
        numbersOnTable = []
        for ball in ballsOnTable: numbersOnTable.append(ball.number)

        allBalls = ballsOnTable
        for i in range(1, 16):
            if i not in numbersOnTable: 
                allBalls.append(Ball([0,0], i, True))
            
        return PoolBoard(cueBall, allBalls)

    def generate_normal_board(self) -> PoolBoard:
        mid_x = Constants.TABLE_WIDTH / 4 - Constants.BALL_RADIUS
        mid_y = Constants.TABLE_HEIGHT / 2

        balls = []
        diameter = 2 * Constants.BALL_RADIUS

        # Randomize the order of the balls but make sure the 8 ball
        # is in the center
        order = []
        for i in range(1, 8):
            order.append(i)

        for i in range(9, 16):
            order.append(i)

        random.shuffle(order)
        order.insert(4, 8)

        # Generate 15 balls placed in a triangle like in a normal
        # billiards game
        for i in range(15):
            x = mid_x
            y = mid_y
            if i == 0:
                pass
            elif i < 3:
                x -= diameter * 0.85
                y += diameter * (i - 2) + Constants.BALL_RADIUS
            elif i < 6:
                x -= 2 * diameter * 0.85
                y += diameter * (i - 4)
            elif i < 10:
                x -= 3 * diameter * 0.85
                y += diameter * (i - 8) + Constants.BALL_RADIUS
            else:
                x = mid_x - 4 * diameter * 0.85
                y += diameter * (i - 12)
            balls.append(Ball([x, y], order[i]))
        
        return PoolBoard(CueBall([Constants.TABLE_WIDTH * 0.75, mid_y]), balls)

    def productionMode(self):
        player1 = ai.RealisticAI(PoolPlayer.PLAYER1)
        player2 = ai.RealisticAI(PoolPlayer.PLAYER2)
        shot_queue = []
        ai_thinking = False
        simulating = False
        fast_forward = False

        board = self.generate_normal_board()
        Pool.WORLD.load_board(board)
        still_frames = 0
        # game loop
        running = True
        while running:

            if not simulating and not ai_thinking and len(shot_queue) == 0:
                target = player1.take_shot if board.turn == PoolPlayer.PLAYER1 else player2.take_shot
                threading.Thread(target=target, args=(board, shot_queue)).start()
                ai_thinking = True
            elif len(shot_queue) > 0:
                ai_thinking = False
                simulating = True
                shot, time = shot_queue.pop()
                
                Pool.WORLD.load_board(board)
                Pool.WORLD.shoot(shot)
            
            if simulating:
                for _ in range(5 if fast_forward else 1):
                    if not Pool.WORLD.update_physics(Constants.TIME_STEP, Constants.VEL_ITERS, Constants.POS_ITERS):
                        still_frames += 1
                    else:
                        still_frames = 0
                graphics = Pool.WORLD.get_graphics()
                if still_frames > 3:
                    board = Pool.WORLD.get_board_state()
                    state = board.get_state()
                    if state == PoolState.ONGOING:
                        print(f"Turn: {board.turn.name}")
                        simulating = False
                    else:
                        print(f"Outcome: {state.name}")
                        board = self.generate_normal_board()
                        simulating = False
                    print(board)
                    Pool.WORLD.load_board(board)

    def testMode(self, magnitudes, angles):
        player1 = ai.RealisticAI(PoolPlayer.PLAYER1, magnitudes, angles)
        player2 = ai.RealisticAI(PoolPlayer.PLAYER2, magnitudes, angles)
        shot_queue = []
        ai_thinking = False
        simulating = False
        fast_forward = True
        
        board = self.generate_normal_board()
        print(f"Turn: {board.turn}")
        Pool.WORLD.load_board(board)
        graphics = Pool.WORLD.get_graphics()

        still_frames = 0
        # game loop
        running = True
        while running:
            
            # Check the event queue
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    # The user closed the window or pressed escape
                    running = False
                elif event.type == VIDEORESIZE:
                    self.screen.screen_height = event.h
                    self.screen.screen_width = event.w
                    self.update_screen()
                    self.screen.screen = pygame.display.set_mode((self.screen.screen_width, self.screen.screen_height), RESIZABLE)
            
            if not simulating and not ai_thinking and len(shot_queue) == 0:
                target = player1.take_shot if board.turn == PoolPlayer.PLAYER1 else player2.take_shot
                threading.Thread(target=target, args=(board, shot_queue)).start()
                ai_thinking = True
            elif len(shot_queue) > 0:
                ai_thinking = False
                simulating = True
                shot, time = shot_queue.pop()
                Pool.WORLD.board.shot = shot.angle
                Pool.WORLD.board.shot_ready = True
                print("shot " + str(shot))

                self.update_graphics(graphics)
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
                        print(f"Turn: {board.turn.name}")
                        simulating = False
                    else:
                        print(f"Outcome: {state.name}")
                        board = self.generate_normal_board()
                        simulating = False

                    print(board)
                    Pool.WORLD.load_board(board)
                    graphics = Pool.WORLD.get_graphics()

            self.update_graphics(graphics)

        print("Done!")   
        pygame.quit()

if __name__ == "__main__":
    
    # production mode
    # pool = Pool(slowMotion=False, graphics=False)
    # pool.productionMode()
    # test mode
    pool = Pool(slowMotion=False, graphics=True)
    magnitudes=[20, 45, 70]
    angles=range(0, 360, 1)
    pool.testMode(magnitudes, angles)


