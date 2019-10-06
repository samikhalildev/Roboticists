from Robot.Robot import Robot
from Model.Yolo_Model import Model

try:
    robot = Robot(Model)
    robot.run()
    
except (RuntimeError, TypeError, NameError, ValueError) as err:
    print('ERROR ---> {0} <---'.format(err))