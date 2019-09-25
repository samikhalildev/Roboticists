import numpy as np
import cv2

cam = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    b, frame = cam.read()

    if b:
        cv2.imshow("Window",frame)
    else:
        print("The camera is not working")
        break
    key = cv2.waitKey(1)&0xFF
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cam.release()