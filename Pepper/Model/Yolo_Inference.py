import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from darkflow.net.build import TFNet
import cv2
import os
import pprint as pp
import subprocess

def classifyImage(data):
    print(data)

def detectImage():
    os.chdir('/home/sami/roboticists/Pepper/Model/DarkflowTry')
    subprocess.call("ls")

    options = {
        "model": "DarkflowTry/cfg/yolov2-tiny.cfg", 
        "load": "DarkflowTry/yolov2-tiny.weights",
        "Train":False,
        "threshold":0.01
    }

    tfnet = TFNet(options)

    original_img = cv2.imread("/home/sami/roboticists/Pepper/item.jpg")
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    results = tfnet.return_predict(original_img)

    return True, results
