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

ORANGE_HUE = 8.71
# YELLOW_HUE = 28.4
ORANGE_AREA_THRESH = 5000
ONE_EIGHTY = 17

# Move forward by 3 encoding
def my_fwd(x=2):
    enc_tgt(1, 0, x)
    fwd()
    sleep(0.1 * x)
    
# Move backward by 3 encoding
def my_bwd(x=2):
    enc_tgt(1, 0, x)
    bwd()
    sleep(0.1 * x)

# Turn right by 1 encoding
def my_right(x=1):
    enc_tgt(1, 0, x)
    right_rot()   
    sleep(0.1 * x) 

# Turn left by 1 encoding
def my_left(x=1):
    enc_tgt(1, 0, x)
    left_rot()
    sleep(0.1 * x)

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

def findLargestBlobArea(bin_img):
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

    return biggest_area

def checkOrange(hsv_frame):
    # 0 to 19, 160 to 255, 220, 255
    lower_color = np.array([ORANGE_HUE-10, 100, 100])
    upper_color = np.array([ORANGE_HUE+10, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    final = filter(mask)
    cv2.imshow("orange", final)
    p_area = findLargestBlobArea(final)
    
    return p_area > ORANGE_AREA_THRESH


def main():
    # Initialize camera and capture first frame
    camera = PiCamera()
    width = 320
    height = 240
    camera.resolution = (width, height)
    rawCapture = picamera.array.PiRGBArray(camera)
    camera.capture(rawCapture, 'bgr')
    frame = rawCapture.array
    
    set_speed(80)
    
    # Prompt user for homography points
    im_source, pts_src = drawRegionCorners(frame)
    assert len(pts_src) == 4
 
    #pts_roadway = np.array([[0,0], [319, 0], [239, 319], [0, 239]])
    
    pts_roadway = np.empty((0, 2), dtype = np.int32)
    pts_roadway = np.append(pts_roadway, [(0, 0)], axis=0)
    pts_roadway = np.append(pts_roadway, [(width, 0)], axis=0)
    pts_roadway = np.append(pts_roadway, [(width, height)], axis=0)
    pts_roadway = np.append(pts_roadway, [(0, height)], axis=0)

    transform, status = cv2.findHomography(pts_src, pts_roadway)

    # Transform the robot position points
    robot_pos = np.array([width / 2, height * 4 / 3, 1])
    roadway_point = transform.dot(robot_pos)
    roadway_x_bot = int(roadway_point[0]/roadway_point[2])
    roadway_y_bot = int(roadway_point[1]/roadway_point[2])
    
    # Transform the robot position points
    robot_pos = np.array([width / 2, 0, 1])
    roadway_point = transform.dot(robot_pos)
    roadway_x_top = int(roadway_point[0]/roadway_point[2])
    roadway_y_top = int(roadway_point[1]/roadway_point[2])
    robot_theta = np.arctan((roadway_x_top - roadway_x_bot) * 1.0 / (roadway_y_top - roadway_y_bot))
    
    print "ROBOT_THETA", robot_theta
    
    while not camera.closed:
        rawCapture = picamera.array.PiRGBArray(camera)
        camera.capture(rawCapture, 'bgr')
        frame = rawCapture.array
        
        im_roadway = cv2.warpPerspective(frame, transform,(width,height))

        cv2.line(im_roadway, (roadway_x_bot,roadway_y_bot), (roadway_x_top,roadway_y_top), (255,0,255),2)  
        
    #     cv2.imshow("homography", im_roadway)
            
        hsv = cv2.cvtColor(im_roadway, cv2.COLOR_BGR2HSV)
        lower_color = np.array([20, 230, 100])
        upper_color = np.array([40, 255, 245])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        final = filter(mask)
#         cv2.imshow("final", final)
        
         
        edges = cv2.Canny(final, 100, 200)
#         cv2.imshow("edges", edges)
    #     cv2.waitKey(0)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 60)
        if lines == None:
            my_right(1)
            continue
        
        dist, angl = 0, 0
        for l in lines:
            for rho, theta in l:
                if theta > np.pi / 2:
                    angl += np.pi - theta
                else:
                    angl += theta
                if rho < 0:
                    dist -= rho
                else:
                    dist += rho
                print rho, theta
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(im_roadway, (x1,y1), (x2,y2), (0,0,255),2)
        dist /= len(lines)
        angl /= len(lines)
        
        print "ANGL", angl * 180 / np.pi
    
        
        if checkOrange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)):  # orange found
            my_left(ONE_EIGHTY)
            continue
    
        x = dist * np.cos(angl)
        print "x",x
        dist_offset = roadway_x_bot - x
        angl_offset = (robot_theta - angl) *  180 / np.pi 

        DIST_THRESHOLD = 40
        ANGL_THRESHOLD = 30
        print "offsets", dist_offset, angl_offset
               
#         cv2.imshow("frame", im_roadway)
#         cv2.waitKey(0)
        if angl_offset > ANGL_THRESHOLD:
            if dist_offset > DIST_THRESHOLD:
                print "case1"
                my_left()
                my_fwd()
            elif dist_offset < -DIST_THRESHOLD:
                print "case2"
                my_fwd()
                my_left()
            else:
                print "case3"
                my_left()
        elif angl_offset < -ANGL_THRESHOLD:
            if dist_offset > DIST_THRESHOLD:
                print "case4"
                my_fwd()
                my_right()
            elif dist_offset < -DIST_THRESHOLD:
                print "case5"
                my_right()
                my_fwd()
            else:
                print "case6"
                my_right()
        else:
            if dist_offset > DIST_THRESHOLD:
                print "case7"
                my_left(2)
                my_fwd(3)
                my_right(2)
            elif dist_offset < -DIST_THRESHOLD:
                print "case8"
                my_right(2)
                my_fwd(3)
                my_left(2)
            else:
                print "case9"
                my_fwd()
    
    cv2.destroyAllWindows()

    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

