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
    - You can greet the robot by saying one of these words: [hi hello hey "hey pepper" "hi pepper" howdy]
    - Find an item by saying: ${item name} OR "looking for $[item name}" OR "scan item"
    - You may use the tablet to interact with the robot.
'''

# Connect robot
session = qi.Session()
robot_ip = '192.168.1.31:9559'
virtual_robot = 'localhost:32913'

session.connect('tcp://' + virtual_robot)
plt.show()

waiting_for_user = True

# Use Pepper services
tts = session.service("ALTextToSpeech")
nav = session.service("ALNavigation")
atts = session.service("ALAnimatedSpeech")

video_proxy = session.service("ALVideoDevice")
dialog = session.service("ALDialog")
memory = session.service("ALMemory")
#magic_tablet = session.service("MagicTablet") #this only works with real robot


# helper functions
def say(text):
    tts.say(text)

def outOfStock(item):
    say('Sorry, ' + item + ' is not in stock.')

def getItemDetails(item):
    item = items[item]
    st1 = 'We have ' + item['productName'] + ' available!'
    st2 = 'You can find it in aisle ' + str(item['aisleNumber']) + '.\nIt is priced for ' + str(item['productPrice'])
    tts.say(st1+st2)
    
    # show on tablet
    # displayDetailsOnTablet(st1, st2)

def displayDetailsOnTablet(st1, st2):
    #html = '<h1>{0}</h1><p style="text-align: center">{1}</p>'.format(st1, st2)
    #magic_tablet.html()
    magic_tablet.show(magic_tablet.animation("TICK"), st1, st2) 
    answer = magic_tablet.ask([(True, "Find another item"), (False, "thank you")])
    
    magic_tablet.show(magic_tablet.animation("TICK"), [], [])
    time.sleep(0.5)
    
    if answer:
        magic_tablet.show(magic_tablet.animation("UNCROSS_HANDS"), "Please scan or tell me another item", [])
        waiting_for_user = True
        getImageEverySec()
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
                htmlElement = None

                if waiting_for_user:
                    htmlElement = '<h2>Hi I am Pepper! You may scan an item or talk to me. :)</h2> <img src="data:image/jpeg;base64,{0}"/>'.format(encoded_data)
                else:
                    htmlElement = '<h1>This is the picture I took, you may retake by saying "scan" again :)</h1> <img src="data:image/jpeg;base64,{0}"/>'.format(encoded_data)
                
                if htmlElement is not None:
                    print(htmlElement)
                   # magic_tablet.html(htmlElement)

    except Exception as e:
        print(e)
    finally:
        proxy.unsubscribe(sub)
    
    return np_image
    
def listen_for(topic):
    result = []
    
    def callback(value):
        if value and len(value) > 0:
            result.append(value)
    
    # Try to unload any topic that already exists
    topics = dialog.getAllLoadedTopics()
    for t in topics:
        try:
            dialog.unloadTopic(t)
        except: 
            pass # do nothing if there was an error

    # Load the new topic
    topic_name = dialog.loadTopicContent(topic)
    
    # Activate the topic and subscribe to user speech
    dialog.activateTopic(topic_name)
    dialog.subscribe('newtopic')
    subscriber = memory.subscriber('Dialog/LastInput')
    subscriber.signal.connect(callback)
    
    # Keep waiting until some results have arrived
    while len(result) == 0:
        time.sleep(0.1)
    
    # Clean up by unloading the topic
    dialog.unsubscribe('newtopic')
    dialog.deactivateTopic(topic_name)
    dialog.unloadTopic(topic_name)
    
    return result[0]

def getImageEverySec():
    if waiting_for_user:
        threading.Timer(1.0, getImageEverySec).start()
        get_frame(video_proxy)

getImageEverySec()

# Begin dialog interaction
interact_topic = """
topic: ~interact()
language: enu

concept:(greeting) [hi hello hey "hey pepper" "hi pepper" howdy]
concept:(looking) ["I am looking for _*" "looking for _*"]
concept:(scanning) [scan take "scan picture" "take picture" "scan item" pic picture]
concept:(items) [chocolate beverage fruit]

u: (_~greeting) Hello there, how may I assist you today?
u: (_~looking) $item=$1
u: (_~items) $item=$1
u: (_~scanning) Scanning item, please wait.
u: (e:Dialog/NotUnderstood) Sorry, item is not in stock. ^stayInScope
"""

say("Hello, what are you looking for today?")

#magic_tablet.html(htmlElement)
while True:
    result = listen_for(interact_topic)
    print('You said:', result)
    
    # if item found, display the details
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
        waiting_for_user = False
        current_frame = get_frame(video_proxy)

        #print(bina/ry.decode('utf-8').replace(u"\u2022", "*"))
        say('Item scanned')

        detectedObject = True #detect(current_frame) -> object location
        say('Item detetcted')

        if detectedObject: 
            item = 'chocolate' #classify(detectedObject) -> chocolate
            say('Classifying item')

            if item and item in items:
                getItemDetails(item)
            else:
                outOfStock('item')
        else:
            say("I couldn't detect the object, please try again.")
                
