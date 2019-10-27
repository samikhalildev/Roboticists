# Roboticists
The majority of retail centres such as shopping malls and supermarkets employ people to assist customers. A lot of customers are introverts and try to avoid contact with the employees that are working in the stores. During busy days, a lot of the customers have to wait for a few minutes to get their questions resolved as there is limited manpower. Apart from that, a lot of the employees face difficulty to search for stock inside the storage room as there are thousands of products. This is time consuming for the customer as well as the employee.

This has a major impact on the customer satisfactory rate and employee’s efficiency levels. Therefore, both these aspects could be balanced by implementing an intelligent application that performs these tasks. A humanoid robot named Pepper was used for this project. Pepper has built in sensors, cameras, microphones and an interactive kiosk. 

This project is designed to assist both staff and customers. The robot is able to interact with people, recognise and assist them finding products. The goal of this project isn't to just locate products but to improve the shopping experience by capturing the interactions and learning from it to alter the robot's behaviour for each person. The robot can then recommend products based on their history, remember past conversations and be their own personalised shopping buddy!

 ![robot](https://user-images.githubusercontent.com/27843440/67614984-ef093000-f811-11e9-8b93-884a1b0f4ec6.png)
 
### Scenario 
 1. Customer: (walks in)
 2. Pepper: Hello there! I am Pepper your shopping assistant, what is your name?
 3. Customer: Sami.
 4. Pepper: Good to meet you Sami! How can I help you today?
 5. Customer: I am looking for a Nikon D500 DSLR Camera.
 6. Pepper: Let me see if we have a Nikon D500 DSLR Camera in stock.
 7. Pepper: Looks like you're in luck today! Aisle 7 on your left.
 8. Customer: Thanks Pepper!
 
### Technologies
 * Object detection (YOLO)
 * Image classification
 * Face recognition
 * Speech recognition
 
 
## How to run

### Setup
 * Setup Ubuntu
 * Install ROS
 * Install PyNaoQi
 * Setup Choregraphe

### Getting started
 This application supports both a virtual and a physical robot.
 To use a virtual robot, simply run Choregraphe and set VIRTUAL_ROBOT constant to True.
    
### Interaction:
 * Speech:
    - Greet the robot by saying: hi, hello or hey pepper
    - To find an item, say: looking for {item} or {item}
    - To see if an item exists, you may can show the robot a picture or a physical object and say: scan item
    - To end interaction, say: bye, laters or see ya

 * Touch:
    - Use the tablet to find a product
    - You may use the tablet to scan an object

 * Recognition:
    - Robot has the capability to detect and recognise humans using feature extraction
    - If the robot doesn't know you, it will ask for your name and extract the features from the frame which will then be stored in a file to recognise you next time.
    - Simply say: do you know me, who am i or what is my name
    
    
