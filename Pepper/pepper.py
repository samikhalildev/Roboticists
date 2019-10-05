# Import dependicies
import qi
from naoqi import ALProxy
from constants import SCAN_ITEM, LOOKING, items, synonyms

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from PIL import Image
from io import BytesIO

import cv2
import pickle
import base64
import threading

''' 
    How to use robot:
    - You can greet the robot by saying one of these words: [hi hello hey howdy]
    - Find an item by saying: ${item name} OR "looking for $[item name}" OR "scan item"
    - You may use the tablet to interact with the robot.
'''

# Connect robot
session = qi.Session()
robot_ip = '192.168.1.41:9559'
virtual_robot = 'localhost:39821'

session.connect('tcp://' + robot_ip)
plt.show()

waiting_for_user = True

# Use Pepper services
tts = session.service("ALTextToSpeech")
nav = session.service("ALNavigation")
atts = session.service("ALAnimatedSpeech")

video_proxy = session.service("ALVideoDevice")
dialog = session.service("ALDialog")
memory = session.service("ALMemory")
magic_tablet = session.service("MagicTablet") #this only works with real robot


# helper functions
def say(text):
    tts.say(text)

def outOfStock(item):
    say('Sorry, ' + item + ' is not in stock.')
    answer = magic_tablet.ask([(True, "Find another item")])
    
    time.sleep(0.5)
    
    if answer:
       beginRobotTablet()

def getItemDetails(item):
    item = items[item]
    st1 = 'We have ' + item['productName'] + ' available!'
    st2 = 'You can find it in aisle ' + str(item['aisleNumber']) + '.\nIt is priced for ' + str(item['productPrice'])
    sentence = st1 + st2
    tts.say(sentence)
    
    # show on tablet
    displayDetailsOnTablet(st1, st2)

def beginRobotTablet():
    magic_tablet.show(magic_tablet.animation("WAVE_HELLO"), "Hi!", "You may scan an item or talk to me :)")
    scan = magic_tablet.ask([(True, "Scan Item"), (False, "Pick item")])
    
    magic_tablet.show(magic_tablet.animation("TICK"), [], [])
    time.sleep(0.5)
    
    if scan:
        scanItem()
    else:
        answer = magic_tablet.ask([("chocolate", "Chocolate"), ("beverage", "beverage"), ("fruit", "fruit")])
        getItemDetails(answer)

def displayDetailsOnTablet(st1, st2):
    magic_tablet.show(magic_tablet.animation("TICK"), st1, st2) 
    answer = magic_tablet.ask([(True, "Find another item"), (False, "thank you")])
    
    magic_tablet.show(magic_tablet.animation("TICK"), [], [])
    time.sleep(0.5)
    
    if answer:
        beginRobotTablet()
    else:
        magic_tablet.show(magic_tablet.animation("UNCROSS_HANDS"), "Goodbye!", [])

def get_frame(proxy, camera_idx=0, resolution_idx=1, colorspace_idx=11, fps=20):
    if not proxy.isCameraOpen(camera_idx):
        proxy.openCamera(camera_idx)

    if not proxy.isCameraStarted(camera_idx):
        video_proxy.startCamera(camera_idx)
    
    if resolution_idx in [3, 4]:
        # max fps for these resolutions
        fps = 1
    
    sub = proxy.subscribeCamera(
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
            result = proxy.getImageRemote(sub)

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
            mpimg.imsave("item.png", np_image)

            with open("item.png", "rb") as image_file:
                encoded_data = base64.b64encode(image_file.read())

    except Exception as e:
        print(e)
    finally:
        proxy.unsubscribe(sub)
    
    return np_image, encoded_data

def stop_listening():
    subscribers = dialog.getSubscribersInfo()
    for sub in subscribers:
        dialog.unsubscribe(sub[0])

    active_topics = dialog.getActivatedTopics()
    for topic in active_topics:
        dialog.deactivateTopic(topic)

    loaded_topics = dialog.getAllLoadedTopics()
    for topic in loaded_topics:
        dialog.unloadTopic(topic)

def listen_for(topic):
    result = []
    stop_listening()

    def callback(value):
        if value and len(value) > 0:
            result.append(value)

    # Load the new topic
    topic_name = dialog.loadTopicContent(topic)
    
    # Activate the topic and subscribe to user speech
    dialog.activateTopic(topic_name)
    dialog.subscribe('newtopic')
    subscriber = memory.subscriber('Dialog/LastInput')
    subscriber.signal.connect(callback)
    
    try:
        # Keep waiting until some results have arrived
        while len(result) == 0:
            time.sleep(0.1)
    finally:
        # Clean up by unloading the topic
        dialog.unsubscribe('newtopic')
        dialog.deactivateTopic(topic_name)
        dialog.unloadTopic(topic_name)
        stop_listening()

    return result[0]

def scanItem():
    current_frame, encoded_data = get_frame(video_proxy)
        
    htmlElement = '<h1 style="text-align:center;">This is the picture I took, you may retake by saying "scan" again :)</h1> <img src="data:image/png;base64,{0}"/>'.format(encoded_data)
    magic_tablet.html(htmlElement, {})
    say('Item scanned')
    
    detectedObject = True #detect(current_frame) -> object location
    #say('Item detetcted')

    if detectedObject: 
        item = 'chocolate' #classify(detectedObject) -> chocolate
        #say('Classifying item')

        if item and item in items:
            getItemDetails(item)
        else:
            outOfStock('item')
    else:
        say("I couldn't detect the object, please try again.")
        
# Begin dialog interaction
interact_topic = """
topic: ~interact()
language: enu

concept:(greeting) [hi hello hey howdy "hey pepper"]
concept:(looking) ["I am looking for _*" "looking for _*"]
concept:(scanning) [scan take "scan picture" "take picture" "scan item" picture]
concept:(items) [chocolate beverage fruit drink]

u: (_~greeting) Hello there, what are you looking for today?
u: (_~items) $item=$1
u: (_~looking) $item=$1
u: (_~scanning) Scanning item, please wait.
u: (e:Dialog/NotUnderstood) Sorry, I dont understand.
"""

beginRobotTablet()

while True:
    result = listen_for(interact_topic)
    print('You said:', result)

    if result in items:
        waiting_for_user = False
        getItemDetails(result)
    
    elif LOOKING in result and result.find('for') != -1:
        index = result.find('for') + 4
        item = result[index:]
        print('item ' + item)
        
        if item in items:
            waiting_for_user = False
            getItemDetails(item)
        else:
            outOfStock(item)
     
    elif result in SCAN_ITEM:
        scanItem()
    
    elif result in ['bye', 'goodbye']:
        stop_listening()
        say('See ya!')

                
