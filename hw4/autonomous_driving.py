from copy import copy
import cv2
import numpy as np
import picamera
from picamera import *
import picamera.array
from gopigo import *
from time import sleep
from cv2 import RHO, waitKey

pts_src = np.empty((0, 2), dtype = np.int32)

ORANGE_HUE = 6
YELLOW_HUE = 28.4

# Move forward by 1 encoding
def my_fwd(x):
    enc_tgt(1, 1, 3)
    fwd()
    
# Move backward by 1 encoding
def my_bwd(x):
    enc_tgt(1, 1, 3)
    bwd()

# Turn right by 1 encoding
def my_right(x):
    enc_tgt(1, 1 ,1)
    right_rot()    

# Turn left by 1 encoding
def my_left(x):
    enc_tgt(1, 1, 1)
    left_rot()

# Mouse handler for select rectangular region
def mouseHandler(event, x, y, flags, param):
    global pts_src
    im_temp = param[0]
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_temp, (x, y), 3, (0, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow("image", im_temp)
        if len(pts_src) < 4:
            pts_src = np.append(pts_src, [(x, y)], axis=0)

"""
Given an image frame, display the image, prompting the user to select rectangular region
"""
def drawRegionCorners(frame):
    cv2.namedWindow("image", 1)
    im_temp = copy(frame)

    cv2.setMouseCallback("image", mouseHandler, [im_temp])
    
    cv2.imshow("image", im_temp)
    cv2.waitKey(0)

    return im_temp, pts_src

"""
Computer mean HSV value coordinates of corners of region
"""
def getHSVThreshold(hsv, min_x, max_x, min_y, max_y):
    m = 0
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            m += hsv[j][i][0]
    m = m * 1.0 / ((max_x - min_x + 1) * (max_y - min_y + 1))
    
    return m

"""
Remove noise and small artifacts from binary image
by applying Gaussian blur, erosion and dilation
"""
def filter(mask):
    # Gaussian blur
    blur = cv2.GaussianBlur(mask, (5,5), 0)
    kernel = np.ones((5,5),np.uint8)

    # Erode then dilate
    final = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
    return final


def main():
    # Initialize camera and capture first frame
    camera = PiCamera()
    width = 320
    height = 240
    camera.resolution = (width, height)
    rawCapture = picamera.array.PiRGBArray(camera)
    camera.capture(rawCapture, 'bgr')
    frame = rawCapture.array
    
    # Prompt user for homography points
    im_source, pts_src = drawRegionCorners(frame)

    pts_roadway = np.array([[0,0], [319,0], [239, 319], [0, 239]])
    transform, status = cv2.findHomography(pts_src, pts_roadway)
    im_roadway = cv2.warpPerspective(frame, transform,(width,height))
    cv2.imshow("homography", im_roadway)
    
    hsv = cv2.cvtColor(im_roadway, cv2.COLOR_BGR2HSV)
    lower_color = np.array([YELLOW_HUE-10, 100, 100])
    upper_color = np.array([YELLOW_HUE+10, 255, 245])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    final = filter(mask)
    cv2.imshow("final", final)
    
    edges = cv2.Canny(final, 100, 200)
    cv2.imshow("edges", edges)
    
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
    print lines
    for l in lines:
        for rho, theta in l:
            print rho, theta
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            print x1,y1,x2,y2
            cv2.line(im_roadway, (x1,y1), (x2,y2), (0,0,255),2)

    cv2.imshow("roadway", im_roadway)
    
    cv2.waitKey(0)    
    
    cv2.destroyAllWindows()

    # Main while loop so GoPiGo continually tracks object
#     while not camera.closed:
#         # Capture new image, threshold, filter and compute new centroid and area
#         rawCapture = picamera.array.PiRGBArray(camera)
#         camera.capture(rawCapture, 'bgr')
#         frame = rawCapture.array
# 
#         # hit the quit key "q" to exit and close everything
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
    # Exit
    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

