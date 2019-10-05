
# Pepper dependiences
import qi
from naoqi import ALProxy

# Custom scripts
from Constants import *
from Tablet import Tablet
from Store import Store
from Model.Yolo_Inference import *

# Helpers
import time
import numpy as np
import cv2
import base64
import random

class Robot:

    def __init__(self):

        self.store = Store()
        self.topic_content = INTERACTION_CONTENT.format(self.store.conceptStringFormat())

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
        This will begin the interaction with the Robot 
    '''
    def run(self):
        #self.startTablet()
        
        while True:
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
                self.say(random.choice(BYE))

                        
    def startTablet(self):
        self.tablet.show(ANIMATION['WAVE'], HI, SCAN_ITEM_OR_TALK)
        answer = self.tablet.ask(SCAN_ITEM, CHOOSE_ITEM)
        
        self.tablet.show(ANIMATION['TICK'])
        time.sleep(0.5)
        
        if answer == SCAN_ITEM:
            self.scanItem()
        else:
            response = self.tablet.ask(self.store.availableItems[:3])
            self.findAndDisplayItem(response)

    def say(self, message):
        self.tts.say(message)

    '''

    '''
    def scanItem(self):
        current_frame, encoded_data = self.get_frame(self)

        self.tablet.html(IMAGE_SCANNED_HTML.format(encoded_data))
        self.say(ITEM_SCANNED)
        
        objectDetected, results = detectImage(current_frame)

        if objectDetected: 
            classifiedImage = classifyImage(results)
            self.findAndDisplayItem(classifiedImage)
        else:
            self.say(OBJECT_NOT_DETECTED)


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
        Displays 2 buttons, Find another item and thank you.
            If find another item was pressed, it will start again
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
                mpimg.imsave("item.jpg", np_image)

                with open("item.jpg", "rb") as image_file:
                    encoded_data = base64.b64encode(image_file.read())

        except Exception as e:
            print(e)

        finally:
            self.video_proxy.unsubscribe(sub)
        
        return np_image, encoded_data