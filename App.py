from Robot.Robot import Robot
from Model.Store import Store
from Model.Yolo_Model import Model
import os

#try:
robot = Robot(os.getcwd(), Store, Model)
robot.run()
    
#except (RuntimeError, TypeError, NameError, ValueError) as err:
    #print('ERROR ---> {0} <---'.format(err))