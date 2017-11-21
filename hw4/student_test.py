from copy import copy
import cv2
import numpy as np
from time import sleep
from cv2 import RHO, waitKey

pts_src = np.empty((0, 2), dtype = np.int32)

ORANGE_HUE = 8.71
YELLOW_HUE = 28.4
ORANGE_AREA_THRESH = 5000
ONE_EIGHTY = 17

# Move forward by 3 encoding
def my_fwd(x=3):
    enc_tgt(1, 1, x)
    fwd()
    
# Move backward by 3 encoding
def my_bwd(x=4):
    enc_tgt(1, 1, x)
    bwd()

# Turn right by 1 encoding
def my_right(x=1):
    enc_tgt(1, 1, x)
    right_rot()    

# Turn left by 1 encoding
def my_left(x=1):
    enc_tgt(1, 1, x)
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
    lower_color = np.array([ORANGE_HUE-10, 100, 100])
    upper_color = np.array([ORANGE_HUE+10, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    final = filter(mask)
    cv2.imshow("orange", final)
    cv2.imwrite("student_captured_image_set/stop_sign_filtered.jpg", final)
    p_area = findLargestBlobArea(final)
    
    return p_area > ORANGE_AREA_THRESH


def main():
    # Initialize camera and capture first frame
    width = 320
    height = 240
    frame = cv2.imread("student_captured_image_set/homography_calibration.jpg")
    
    # Prompt user for homography points
    im_source, pts_src = drawRegionCorners(frame)
    assert len(pts_src) == 4
    
    pts_roadway = np.empty((0, 2), dtype = np.int32)
    pts_roadway = np.append(pts_roadway, [(0, 0)], axis=0)
    pts_roadway = np.append(pts_roadway, [(width, 0)], axis=0)
    pts_roadway = np.append(pts_roadway, [(width, height)], axis=0)
    pts_roadway = np.append(pts_roadway, [(0, height)], axis=0)
    
    transform, status = cv2.findHomography(pts_src, pts_roadway)

    frame = cv2.imread("student_captured_image_set/original_image.jpg")

    while True:
        im_roadway = cv2.warpPerspective(frame, transform,(width,height))
        cv2.imwrite("student_captured_image_set/homography_applied.jpg", im_roadway)

        # Transform the robot position points
        robot_pos = np.array([width / 2, height * (22.5+13.5)/22.5, 1])
        roadway_point = transform.dot(robot_pos)
        roadway_x_bot = int(roadway_point[0]/roadway_point[2])
        roadway_y_bot = int(roadway_point[1]/roadway_point[2])
        
        # Transform the robot position points
        robot_pos = np.array([width / 2, 0, 1])
        roadway_point = transform.dot(robot_pos)
        roadway_x_top = int(roadway_point[0]/roadway_point[2])
        roadway_y_top = int(roadway_point[1]/roadway_point[2])  
        
    #     cv2.imshow("homography", im_roadway)
            
        hsv = cv2.cvtColor(im_roadway, cv2.COLOR_BGR2HSV)
        lower_color = np.array([YELLOW_HUE-10, 230, 100])
        upper_color = np.array([YELLOW_HUE+10, 255, 245])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        final = filter(mask)
        cv2.imshow("final", final)
        cv2.imwrite("student_captured_image_set/yellow_color_filtered.jpg", final)
        
         
        edges = cv2.Canny(final, 100, 200)
        cv2.imshow("edges", edges)
    #     cv2.waitKey(0)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 60)
        dist, angl = 0, 0
        for l in lines:
            for rho, theta in l:
                dist = rho
                angl = theta
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(im_roadway, (x1,y1), (x2,y2), (0,0,255),2)

        cv2.imwrite("student_captured_image_set/calculated_hough_lines.jpg", im_roadway)
    
        if checkOrange(hsv):  # orange found
            sleep(0.7)
    
        if len(lines) != 0:
            x = (dist - height * np.sin(angl)) / np.cos(angl)
            dist_offset = roadway_x_bot - x
            slope = (roadway_y_top - roadway_y_bot) / (roadway_x_top - roadway_x_bot)
            b = roadway_y_top - slope * roadway_x_top 
            y = slope * x + b
            angl_offset = np.arctan((roadway_x_top - x) / (roadway_y_top - y))
    
        print 'calculated_angle_offset = ', angl_offset
        print 'calculated_distance_offset = ', dist_offset
        DIST_THRESHOLD = 50
        ANGL_THRESHOLD = 0.5
               
        break
    print 'homography_transform_matrix = '
    print transform
    print "distance_to_camera_from_homography = 31"
    cv2.destroyAllWindows()

    # Exit
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

