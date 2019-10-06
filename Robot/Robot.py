
# Pepper dependiences
import qi
from naoqi import ALProxy

# Custom scripts
from Constants import *
from Tablet import Tablet

# Helpers
import time, cv2, base64, random, os, subprocess, sys
import numpy as np
import matplotlib.image as mpimg

class Robot:

    def __init__(self, Model, Store):

        self.path = os.getcwd()
        self.imagePath = self.path + IMAGE_PATH

        self.store = Store()
        self.items = self.store.availableItems

        self.model = Model(self.items)

        # Connect Robot
        self.session = qi.Session()
        self.robot_ip = REAL_ROBOT_IP

        if VIRTUAL_ROBOT:
            self.robot_ip = VIRTUAL_ROBOT_IP

        self.session.connect('tcp://{0}'.format(self.robot_ip))

        # Use Pepper services
        self.tts = self.session.service("ALTextToSpeech")
        self.nav = self.session.service("ALNavigation")
        self.atts = self.session.service("ALAnimatedSpeech")
        self.video_proxy = self.session.service("ALVideoDevice")
        self.dialog = self.session.service("ALDialog")
        self.memory = self.session.service("ALMemory")
        
        if not VIRTUAL_ROBOT:
            self.tablet = Tablet(self.session)

    '''
        This will start the interaction with the Robot 
        It consistently listen for user input
    '''
    def run(self):
        #self.startTablet()

        while True:
            self.createContentTopic()
            result = self.listen_for(self.topic_content)

            print('You said: {0}'.format(result))

            foundItem = self.store.getItem(result)

            if foundItem:
                self.displayProduct(foundItem)

            elif LOOK_FOR in result and result.find(FOR) != -1:
                index = result.find(FOR) + 4
                item = result[index:]
                print('item ' + item)
                
                self.findAndDisplayItem(item)
            
            elif result in SCAN:
                self.scanItem()
            
            elif result in BYE:
                self.stop_listening()


    # Generate random values for the robot to listen and say
    def createContentTopic(self):
        self.topic_content = INTERACTION_CONTENT.format(
            self.conceptStringFormat(USER_GREET),
            random.choice(ROBOT_GREET),
            self.conceptStringFormat(LOOK),
            self.conceptStringFormat(self.items),
            self.conceptStringFormat(SCAN),
            self.conceptStringFormat(BYE),
            random.choice(BYE),
            random.choice(ROBOT_CONFUSED)
        )

    '''
        Display two buttons to the user
            - Scan item and choose item
                - if scan item was pressed, it will call the scanItem function to detect and classify the item
                - if choose item was pressed, it will display available items and when pressed it will show the item details
    '''
    def startTablet(self):
        self.tablet.show(ANIMATION['WAVE'], HI, SCAN_ITEM_OR_TALK)
        answer = self.tablet.ask(SCAN_ITEM, CHOOSE_ITEM)
        
        self.tablet.show(ANIMATION['TICK'])
        time.sleep(0.5)
        
        if answer == SCAN_ITEM:
            self.scanItem()
        else:
            response = self.tablet.ask(self.items[:3])
            self.findAndDisplayItem(response)

    def say(self, message):
        self.tts.say(message)

    '''
        - Get the current frame from the robot camera
        - Encodes the frame into base64 to display on the tablet
        - Call method in model to classify image
        - If the classifed value is available, display details
    '''
    def scanItem(self):
        current_frame, encoded_data = self.get_frame()
        print(encoded_data)

        imageSrc = IMAGE_SCANNED_HTML.format(encoded_data)
        #self.tablet.htmlDisplay(imageSrc)
        self.say(ITEM_SCANNED)
        
        item = self.model.getItemFromImage()

        if item is not None: 
            print('Item classified is: {0}'.format(item))
            self.findAndDisplayItem(item)
        else:
            self.say(OBJECT_NOT_DETECTED)

    '''
        - Check the store if the item is available and display it
    '''
    def findAndDisplayItem(self, item):
        itemInStock = self.store.getItem(item)
        if itemInStock:
            self.displayProduct(itemInStock)
            return True
        else:
            self.outOfStock(item)
            return False

            
    def displayProduct(self, item):
        productName = item['productName']
        productPrice = item['productPrice']

        line1 = ITEM_AVAILABLE.format(productName)
        line2 = AISLE.format(productName, productPrice)
        
        message = line1 + line2

        self.say(message)

        #self.tablet.display(ANIMATION['TICK'], line1, line2)
        #self.findAnotherItem()


    def outOfStock(self, item):
        self.say(NOT_IN_STOCK.format(item))
        #self.findAnotherItem()

    '''
        - Displays 2 buttons, Find another item and thank you.
            - If find another item was pressed, it will start again
    '''
    def findAnotherItem(self):
        answer = self.tablet.ask(FIND_ANOTHER_ITEM, THANK_YOU)

        self.tablet.show(ANIMATION['TICK'])
        time.sleep(0.5)

        if answer is FIND_ANOTHER_ITEM:
            self.startTablet()
        else:
            self.tablet.show(ANIMATION['UNCROSS_HANDS'], random.choice(BYE))
            self.stop_listening()
            self.say(random.choice(BYE))

    def conceptStringFormat(self, data):
        string = ''
        for item in data:
            string += '"{0}" '.format(item)
        return string

    def listen_for(self, topic):
        result = []
        self.stop_listening()

        def callback(value):
            if value and len(value) > 0:
                result.append(value)

        # Load the new topic
        topic_name = self.dialog.loadTopicContent(topic)
        
        # Activate the topic and subscribe to user speech
        self.dialog.activateTopic(topic_name)
        self.dialog.subscribe('newtopic')
        subscriber = self.memory.subscriber('Dialog/LastInput')
        subscriber.signal.connect(callback)
        
        try:
            # Keep waiting until some results have arrived
            while len(result) == 0:
                time.sleep(0.1)
        finally:
            # Clean up by unloading the topic
            self.dialog.unsubscribe('newtopic')
            self.dialog.deactivateTopic(topic_name)
            self.dialog.unloadTopic(topic_name)
            self.stop_listening()

        return result[0]


    def stop_listening(self):
        subscribers = self.dialog.getSubscribersInfo()
        for sub in subscribers:
            self.dialog.unsubscribe(sub[0])

        active_topics = self.dialog.getActivatedTopics()
        for topic in active_topics:
            self.dialog.deactivateTopic(topic)

        loaded_topics = self.dialog.getAllLoadedTopics()
        for topic in loaded_topics:
            self.dialog.unloadTopic(topic)


    def get_frame(self, camera_idx=0, resolution_idx=1, colorspace_idx=11, fps=20):
        if not self.video_proxy.isCameraOpen(camera_idx):
            self.video_proxy.openCamera(camera_idx)

        if not self.video_proxy.isCameraStarted(camera_idx):
            self.video_proxy.startCamera(camera_idx)
        
        if resolution_idx in [3, 4]:
            fps = 1
        
        sub = self.video_proxy.subscribeCamera(
            "get_frame_sub",
            camera_idx,
            resolution_idx,
            colorspace_idx,
            fps
        )
        
        np_image = None
        encoded_data = None

        try:
            timeout = 3
            start_time = time.time()
            result = None
            while time.time() - start_time < timeout and result is None:
                result = self.video_proxy.getImageRemote(sub)

            if result:
                buffer_image = result[6]

                if result[2] == 3:
                    img_shape = (result[1], result[0], result[2])
                    im_format = np.uint8
                else:
                    img_shape = (result[1], result[0])
                    im_format = np.uint8
                
                temp = np.frombuffer(buffer_image, im_format)
                np_image = np.reshape(temp, img_shape)
                #mpimg.imsave("dasdasd.jpg", np_image)
                #cv2.imwrite(self.imagePath, np_image)
                
                with open(self.imagePath, "rb") as image_file:
                    encoded_data = base64.b64encode(image_file.read())

        except Exception as e:
            print(e)

        finally:
            self.video_proxy.unsubscribe(sub)
        
        return np_image, encoded_data