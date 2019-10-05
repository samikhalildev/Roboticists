from Robot import Robot

''' 
    How to use Pepper:
    - Greet the robot by saying one of these words: [hi hello hey howdy]
    - Find an item by saying: ${item name} OR "looking for $[item name}" OR "scan item"
    - You may use the tablet to interact with the robot.
'''

#try:
robot = Robot()
robot.run()

#except (RuntimeError, TypeError, NameError, ValueError) as err:
    #print('ERROR ---> {0} <---'.format(err))