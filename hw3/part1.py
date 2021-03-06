#simple python OpenCv program to read in a frame from a webcam, write the frame into a video file,
#and display each frame (live video)
#output video is "output.avi" - make sure you turn the camera OFF or this file gets BIG!
# see Chapter 1 in:
#https://media.readthedocs.org/pdf/opencv-python-tutroals/latest/opencv-python-tutroals.pdf

import argparse
from copy import deepcopy as copy

import cv2

import numpy as np


#import imutils
#from test.test_typechecks import Integer
def mouseHandler(event, x, y, flags, param):
    global im_temp, pts_src
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_temp, (x, y), 3, (0, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow("image", im_temp)
        if len(pts_src) < 4:
            pts_src = np.append(pts_src, [(x, y)], axis=0)     
 
#Open the webcam, typically device 0, if multiple webcams use 0,1,2,....
 
cap = cv2.VideoCapture(0) 

# Capture a frame
ret, frame = cap.read()

# Create a named window
 
cv2.namedWindow("image", 1)
im_temp = frame.copy()
pts_src = np.empty((0, 2), dtype = np.int32)
cv2.setMouseCallback("image", mouseHandler)
 
cv2.imshow("image", im_temp)
cv2.waitKey(0)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

min_x = float("inf")
max_x = -1
min_y = float("inf")
max_y = -1
 
for i in pts_src:
    min_x = min(i[0], min_x)
    max_x = max(i[0], max_x)
    min_y = min(i[1], min_y)
    max_y = max(i[1], max_y)
 
cv2.rectangle(im_temp, (min_x,min_y), (max_x, max_y), (0, 255, 255))
cv2.imshow("image", im_temp)
# cv2.imshow("hsv", hsv)


m = 0
for i in range(min_x, max_x + 1):
    for j in range(min_y, max_y + 1):
        m += hsv[j][i][0]
avg = m * 1.0 / ((max_x - min_x + 1) * (max_y - min_y + 1))
print avg

lower_color = np.array([avg-10, 50, 50])
upper_color = np.array([avg+10, 255, 255])

mask = cv2.inRange(hsv, lower_color, upper_color)
res = cv2.bitwise_and(frame, frame, mask=mask)

cv2.imshow("mask", mask)

# Filtering
blur = cv2.GaussianBlur(mask, (5,5), 0)
kernel = np.ones((5,5),np.uint8)
final = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)

cv2.imshow("filter", final)

x_avg = 0
y_avg = 0
for i in range(len(final)):
    for j in range(len(final[i])):
        if final[i][j]:
            x_avg += j
            y_avg += i
            
x_avg /= len(final[0])
y_avg /= len(final)

im2, contours, hierarchy = cv2.findContours(final,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

biggest_contour = 0
biggest_area = -1
for i in contours:
    if cv2.contourArea(i) > biggest_area:
        biggest_area = cv2.contourArea(i)
        biggest_contour = copy(i)

M = cv2.moments(biggest_contour)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

cv2.circle(res, (cx, cy), 3, (0, 255, 255), 5, cv2.LINE_AA)

cv2.imshow("mask", res)

cv2.waitKey(0)
cv2.destroyAllWindows()