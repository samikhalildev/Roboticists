# Roboticists


## Setup:
    This application supports both a virtual and a physical robot. 
    To use a virtual robot, simply run Choregraphe and set VIRTUAL_ROBOT constant to True. However, there may be some issues using 
    the virtual robot as the tablet service is not supported.
    
## Interaction:
    Speech:
        - Greet the robot by saying: hi, hello or hey pepper
        - To find an item, say: looking for {item} or {item}
        - To see if an item exists, you may can show the robot a picture or a physical object and say: scan item
        - To end interaction, say: bye, laters or see ya

    Touch:
        - Use the tablet to find a product
        - You may use the tablet to scan an object

    Recognise:
        - Robot has the capability to detect and recognise humans using feature extraction
        - If the robot doesn't know you, it will ask for your name and extract the features from the frame which will then be stored in a file to recognise you next time.
        - To begin this, say: do you know me, who am i or what is my name"