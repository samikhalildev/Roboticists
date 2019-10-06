from Robot.Robot import Robot
from Model.Yolo_Model import Model
from Model.Store import Store

try:
    robot = Robot(Model, Store)
    robot.run()
    
except (RuntimeError, TypeError, NameError, ValueError) as err:
    print('ERROR ---> {0} <---'.format(err))