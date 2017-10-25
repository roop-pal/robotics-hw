#simple python OpenCv program to read in a frame from a webcam, write the frame into a video file,
#and display each frame (live video)
#output video is "output.avi" - make sure you turn the camera OFF or this file gets BIG!
# see Chapter 1 in:
#https://media.readthedocs.org/pdf/opencv-python-tutroals/latest/opencv-python-tutroals.pdf

import numpy as np
import argparse
#import imutils
import cv2

def mouseHandler(event,x,y,flags,param):
    global im_temp, pts_src
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_temp,(x,y),3,(0,255,255),5,cv2.LINE_AA)
        cv2.imshow("image", im_temp)
        if len(pts_src) < 4:
            pts_src = np.append(pts_src,[(x,y)],axis=0)     

#Open the webcam, typically device 0, if multiple webcams use 0,1,2,....

cap = cv2.VideoCapture(0) 

# Open webcam
cap = cv2.VideoCapture(0)

# Capture a frame
ret, frame = cap.read()

# Create a named window

cv2.namedWindow("image",1)
im_temp=frame
pts_src= np.empty((0,2),dtype=np.int32)
cv2.setMouseCallback("image",mouseHandler)

cv2.imshow("image",im_temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
print pts_src
 
