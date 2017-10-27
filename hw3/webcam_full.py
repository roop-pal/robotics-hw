from copy import deepcopy as copy
import cv2
import numpy as np

pts_src = np.empty((0, 2), dtype = np.int32)

def my_fwd(x):
    print "fwd", x

def my_bwd(x):
    print "bwd", x
    
def my_right(x):
    print "right", x
    
def my_left(x):
    print "left", x

def mouseHandler(event, x, y, flags, param):
    global pts_src
    im_temp = param[0]
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_temp, (x, y), 3, (0, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow("image", im_temp)
        if len(pts_src) < 4:
            pts_src = np.append(pts_src, [(x, y)], axis=0)

def drawRegionCorners(frame):
    cv2.namedWindow("image", 1)
    im_temp = frame.copy()

    cv2.setMouseCallback("image", mouseHandler, [im_temp])
    
    cv2.imshow("image", im_temp)
    cv2.waitKey(0)

    return im_temp, pts_src

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

def getHSVThreshold(hsv, min_x, max_x, min_y, max_y):
    m = 0
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            m += hsv[j][i][0]
    m = m * 1.0 / ((max_x - min_x + 1) * (max_y - min_y + 1))
    
    return m


def filter(mask):
    # Gaussian blur
    blur = cv2.GaussianBlur(mask, (5,5), 0)
    kernel = np.ones((5,5),np.uint8)

    # Erode then dilate
    final = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
    return final

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
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret == True:
        im_region, pts_src = drawRegionCorners(frame)
    else:
        print "could not get frame"
        return 0

    [min_x, max_x, min_y, max_y] = getCorners(pts_src)

    cv2.destroyAllWindows()
    # imcopy = frame.copy()
    # cv2.rectangle(imcopy, (min_x,min_y), (max_x, max_y), (0, 255, 255))
    # cv2.imshow("region", imcopy)
    # cv2.waitKey(0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_mean = getHSVThreshold(hsv, min_x, max_x, min_y, max_y)
    lower_color = np.array([hsv_mean-10, 50, 50])
    upper_color = np.array([hsv_mean+10, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    #cv2.imshow("mask", mask)

    final = filter(mask)
    (cx, cy, p_area) = findLargestBlob(final)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.circle(res, (cx, cy), 3, (0, 255, 255), 5, cv2.LINE_AA)
    cv2.imshow("centroid", res)
    #cv2.waitKey(0)

    while (cap.isOpened()):
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        final = filter(mask)
        (cx, cy, area) = findLargestBlob(final)
        cv2.circle(frame, (cx, cy), 3, (0, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow("centroid", frame)
        
        if (len(frame[0]) / 2 - cx > 20):
            my_left(len(frame[0]) / 2 - cx)
        elif (len(frame[0]) / 2 - cx < -20):
            my_right(cx - len(frame[0]) / 2)
        elif ((p_area - area) / p_area > 0.1):
            my_fwd((p_area - area) / p_area)
        elif ((p_area - area) / p_area < -0.1):
            my_bwd((area - p_area) / p_area)
        else:
            print "dont move"

        # hit the quit key "q" to exit and close everything
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
