import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from darkflow.net.build import TFNet
import pprint as pp
import sys, os, subprocess, cv2

class Model:

    def __init__(self, items):
        self.path = os.getcwd()
        
        if self.path.find('Model') is -1:
            self.path += '/Model'
        
        self.image_path = self.path + '/img/item.jpg'
        self.yolo_tiny_path = self.path + '/DarkflowTry/cfg/yolov2-tiny.cfg'
        self.yolo_weights_path = self.path + '/yolov2-tiny.weights'
        self.availableItems = items

        os.chdir(self.path + '/DarkflowTry')

        self.options = {
            "model": self.yolo_tiny_path, 
            "load": self.yolo_weights_path,
            "Train": False,
            "threshold": 0.01
        }

        self.tfnet = TFNet(self.options)
        self.result = []

    def getItemFromImage(self):
        detected = self.detectImage()

        if detected:
            return self.classifyImage()
        else:
            return None

    def detectImage(self):
        try:
            original_img = cv2.imread(self.image_path)
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            self.result = self.tfnet.return_predict(original_img)

            return len(self.result)

        except (RuntimeError, TypeError, NameError, ValueError) as err:
            print(err)
            return False

    def classifyImage(self):
        print('\nImage location: {0}'.format(self.image_path))
        print("Total objects detected: {0}".format(len(self.result)))

        itemsFound = []

        for data in self.result:
            label = str(data['label']).lower()
            value = data['confidence']
            print(label)

            if label in self.availableItems:
                itemsFound.append((label, value))

        return self.getHighestValue(itemsFound)

    def getHighestValue(self, itemsFound):
        label = None
        value = 0
        print('\nItems detected that are available in store: {0}'.format(itemsFound))

        for item in itemsFound:
            if item[1] > value:
                label, value = item[0], item[1]

        return label

if __name__ == "__main__":
    items = ['chocolate', 'beverages', 'fruit', 'banana', 'juice', 'orange', 'strawberry', 'blueberry', 'watermelon', 'peach', 'pear', 'beverages', 'pods', 'mars', 'mars pods', 'apple', 'pepsi', 'cola', 'soft drink', 'drink']
    value = Model(items).getItemFromImage()
    print('Value: {0}'.format(label))