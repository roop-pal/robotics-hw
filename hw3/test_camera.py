#simple python OpenCv program to read in a frame from a webcam, write the frame into a video file,
#and display each frame (live video)
#output video is "output.avi" - make sure you turn the camera OFF or this file gets BIG!
# see Chapter 1 in:
#https://media.readthedocs.org/pdf/opencv-python-tutroals/latest/opencv-python-tutroals.pdf

import numpy as np
import argparse
#import imutils
import cv2

#Open the webcam, typically device 0, if multiple webcams use 0,1,2,....

cap = cv2.VideoCapture(0) 

#set up output video compression method, output file, frame rate and image size

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # write and display the frame
        out.write(frame)
        cv2.imshow('frame',frame)
        
        # hit the quit key "q" to exit and close everything
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()