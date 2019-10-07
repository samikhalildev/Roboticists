from .network import inference as _inference
from .estimator import PoseEstimator as _PoseEstimator

from .body_parts import *

def detect(img):
    '''
    Uses OpenPose to detect people in a supplied n*m*3 uint8 image.
    
    This class is based on MobileNet OpenPose:
    https://github.com/ildoonet/tf-pose-estimation

    Input: a numpy array (n*m*3) of RGB data
    
    Output: a list of dictionaries mapping from part names to image coordinates
    '''
    # Get the image dimensions
    height = img.shape[0]
    width = img.shape[1]
    # Perform neural network inference
    output = _inference(img)
    heatMat = output[:, :, :19]
    pafMat = output[:, :, 19:]
    # Recognize body parts in the network output
    humans = _PoseEstimator.estimate(heatMat, pafMat)
    # Flatten the result into a simple data structure:
    # [{part_number:(x_coordinate, y_coordinate)}]
    results = []
    for human in humans:
        parts = {}
        for part, info in human.body_parts.items():
            parts[part] = (int(info.x * width), int(info.y * height))
        results.append(parts)
    return results
