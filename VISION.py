import src.ShotSelection.run_single_production_mode as ShotSelectionProd
import src.ShotSelection.run_single_test_mode as ShotSelectionTest

from src.ShotSelection.pool_objets import Ball, CueBall, PoolPlayer
from src.ShotSelection.pool import Pool
from src.HoughCircle import DetectCircles
from src.AnkerCameraLibrary import AnkerCamera
from src.BluetoothServer import BluetoothServerSocket
from src.GameState import InvalidBallCount, DetectShot
from src.Ball import BallConvertor

def main():

    # Initialize game variables
    Startup = True
    Continue = True
    Current_Ball_List = None
    Previous_Ball_List = None

    # Initialize connections
    # myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
    # pi_bluetooth_socket = BluetoothServerSocket(10) # Port 10 (arbitrary choice)
    # myCam.take_video()

    while(Continue):
        # Begin computer vision
        # myCam = AnkerCamera(2) # 1 on Jetson Nano; 2 on laptop
        # myCam.take_picture()
        Current_Ball_List = DetectCircles()
  
        # Player 1 is solids and Player 2 is stripes
        playerTurn = PoolPlayer.PLAYER1
        ##########################################

        pool = Pool(slowMotion=False, graphics=True)
        magnitudes = [45, 75, 90]
        angles = range(0, 360, 1)
  
        ballsProd = list()
        convertor = BallConvertor(pool.screen.ppm)
        
        cueBallProd = CueBall((0,0))
        
        for ball in Current_Ball_List:
            convertedBall = convertor.convertBall(ball)
            if convertedBall is not None:
                if convertedBall.number == 0:
                    cueBallProd = convertedBall
                else:
                    ballsProd.append(convertedBall)
                print(ball.color)
                print(str(ball.x) + " " + str(ball.y))
       
        ShotSelectionTest.runSingleTestMode(
              balls=ballsProd, 
                cueBall=cueBallProd, 
             magnitudes=magnitudes, 
              angles=angles, 
               pool_sim=pool, 
            turn=playerTurn
          )
            

             
        if Previous_Ball_List is not None:
            try:
                ret = DetectShot(Previous_Ball_List, Current_Ball_List)
                # Need to add shot outcome logic in here
                print(ret)

            except InvalidBallCount:
                print("Invalid ball count, something is wrong")
            break

        # Current shot is complete, store current game state
        Previous_Ball_List = Current_Ball_List

        Startup = False


if __name__ == "__main__":
    main()
