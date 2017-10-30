from copy import copy
import cv2
import numpy as np
import picamera
from picamera import *
import picamera.array
from gopigo import *
from time import sleep

pts_src = np.empty((0, 2), dtype = np.int32)

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
Given the four user-chosen points, return corners of approximated rectangular region
"""
def getCorners(pts_src):
    min_x = float("inf")
    max_x = -1
    min_y = float("inf")
    max_y = -1
 
    for i in pts_src:
        min_x = min(i[0], min_x)
        max_x = max(i[0], max_x)
        min_y = min(i[1], min_y)
        max_y = max(i[1], max_y)

    return [min_x, max_x, min_y, max_y]

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

"""
Return coordinates of centroid and area of largest blob in a binary image
"""
def findLargestBlob(bin_img):
    x_avg = 0
    y_avg = 0
    for i in range(len(bin_img)):
        for j in range(len(bin_img[i])):
            if bin_img[i][j]:
                x_avg += j
                y_avg += i
            
    x_avg /= len(bin_img[0])
    y_avg /= len(bin_img)

    im2, contours, hierarchy = cv2.findContours(bin_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    biggest_contour = 0
    biggest_area = -1
    for i in contours:
        if cv2.contourArea(i) > biggest_area:
            biggest_area = cv2.contourArea(i)
            biggest_contour = copy(i)

    M = cv2.moments(biggest_contour)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy, biggest_area)


def main():
    # Initialize camera and capture first frame
    camera = PiCamera()
    camera.resolution = (320, 240)
    rawCapture = picamera.array.PiRGBArray(camera)
    camera.capture(rawCapture, 'bgr')
    frame = rawCapture.array
    
    # Prompt user for region to track
    im_region, pts_src = drawRegionCorners(frame)

    # Calculate corners of a rectangle from input region
    [min_x, max_x, min_y, max_y] = getCorners(pts_src)

    cv2.destroyAllWindows()

    # Threshold the image based on average hue of region
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_mean = getHSVThreshold(hsv, min_x, max_x, min_y, max_y)
    lower_color = np.array([hsv_mean-10, 50, 50])
    upper_color = np.array([hsv_mean+10, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    #cv2.imshow("mask", mask)

    # Filter the mask and display centroid overlayed onto original frame
    final = filter(mask)
    (cx, cy, p_area) = findLargestBlob(final)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.circle(res, (cx, cy), 3, (0, 255, 255), 5, cv2.LINE_AA)
    cv2.imshow("centroid", res)
    #cv2.waitKey(0)

    # Main while loop so GoPiGo continually tracks object
    while not camera.closed:
        # Capture new image, threshold, filter and compute new centroid and area
        rawCapture = picamera.array.PiRGBArray(camera)
        camera.capture(rawCapture, 'bgr')
        frame = rawCapture.array
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        final = filter(mask)
        (cx, cy, area) = findLargestBlob(final)
        cv2.circle(frame, (cx, cy), 3, (0, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow("centroid", frame)

        # Move robot according to newly measured centroid and area
        if (len(frame[0]) / 2 - cx > 30):
            my_left(len(frame[0]) / 2 - cx)
        elif (len(frame[0]) / 2 - cx < -30):
            my_right(cx - len(frame[0]) / 2)
        elif ((p_area - area) / p_area > 0.1):
            my_fwd((p_area - area) / p_area)
        elif ((p_area - area) / p_area < -0.1):
            my_bwd((area - p_area) / p_area)
        else:
            print "dont move"
	sleep(0.2)
        # hit the quit key "q" to exit and close everything
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Exit
    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

