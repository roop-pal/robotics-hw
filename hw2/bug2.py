from gopigo import *
from time import *
import math
import numpy as np
import matplotlib.pyplot as plt

# Constants based on robots for accurate turning and moving
threesixty = 39.0
WHEEL_RAD = 3.25

BUG_POS = [0, 0, 90, 0] # x, y, theta, object_detected
MAP = [BUG_POS] # list of bug positions

# Turn left a certain amount
def left_deg(deg):
    if deg < 0:
	right_deg(-deg)
        return
    # Update bug position and map
    BUG_POS[2] += deg
    MAP.append(list(BUG_POS))
    # Turn
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        left_rot()
    stop()

# Turn right a certain amount, similar to left_deg()
def right_deg(deg):
    if deg < 0:
	left_deg(-deg)
        return
    BUG_POS[2] -= deg
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        right_rot()
    stop()

# Move forward a certain amount
def fwd_cm(dist):
    # Update bug position and map
    BUG_POS[0] += dist * math.cos(math.radians(BUG_POS[2]))
    BUG_POS[1] += dist * math.sin(math.radians(BUG_POS[2]))
    MAP.append(list(BUG_POS))
    # Move
    enc_tgt(1, 1, cm2pulse(dist))
    while read_enc_status():
        fwd()
    stop()

# Converts cm to pulses for fwd_cm()
def cm2pulse(dist):
    return int(dist / (2 * math.pi * WHEEL_RAD) * 18)

# Calculates euclidean distance for isatpoint(), looks only at first two parts of given vectors
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Returns if two points are close enough together to be considered at the same point    
def isatpoint(p1, p2):
    if dist(p1, p2) < 3:
        return True
    return False

# Draws MAP. Red used to signify obstacle detected, blue used to signify no obstacle detected
def draw_map():
    print(len(MAP))
    x, y, u, v, colors = [], [], [], [], []
    # Convert data into quiver-digestable lists
    for i in MAP:
        x.append(i[0])
        y.append(i[1])
	# Convert theta into arrow's x and y coords
        u.append(math.cos(math.radians(i[2])))
        v.append(math.sin(math.radians(i[2])))
	if i[3]:
	    colors.append((1, 0, 0))
	else:
    	    colors.append((0, 0, 1))
    plt.figure()
    ax = plt.gca()
    ax.quiver(x, y, u, v, colors)
    plt.draw()
    plt.show()

# Bug 2 algorithm
def bug2(Q_GOAL):
    while True:
	# Move fwd until object detected
        while (us_dist(15) > 10):
            fwd_cm(5)
            sleep(0.2)
	    # If goal is reached on way to obstacle
            if dist(BUG_POS, Q_GOAL) < 6:
                return True
	# Obstacle detected, updated BUG_POS value
	BUG_POS[3] = 1
	# Start left-leaning border following alg
        left_deg(90)
	BUG_POS[3] = 0
	# Store hit_point
        hit_point = list(BUG_POS)

        while True:
	    # Measure right of robot
            servo(0)
            sleep(0.2)
            right = us_dist(15)
	    # Measure fwd of robot
            servo(90)
            sleep(0.2)
            forward = us_dist(15)
            # Right sensor and fwd sensor tests to determine movement
	    # All fwd_cm() calls are using the robot's coordinate system, so the actual movements are off by a factor of 1.3
	    # If too close to right, turn left and move forward
            if right < 10:
		BUG_POS[3] = 1
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
            if not right < 25:
		# If nothing found on right, check right-forward diagonal
                servo(45)
                sleep(0.2)
		# If too close on diagonal, turn left and move forward
                if us_dist(15) < 25:
		    BUG_POS[3] = 1
                    left_deg(30)
                    sleep(0.25)
                    fwd_cm(3)
                    sleep(0.25)
                # If nothing on right side is found, move forward and turn right
		else:
                    fwd_cm(3)
                    sleep(0.25)
                    right_deg(30)
                    sleep(0.25)
	    # If forward and right sides find obstacles, turn left and move forward
            elif forward < 25:
		BUG_POS[3] = 1
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
	    # If right obstacle detected but front clear, move forward
            else:
		BUG_POS[3] = 1
                fwd_cm(5)
                sleep(0.25)
	    # Print BUG_POS for debugging
	    print BUG_POS
        
	    # If goal is found after a move, report True
            if dist(BUG_POS, Q_GOAL) < 6:
                return True
	    # If hit point re-encountered, conclude impossible
            if isatpoint(BUG_POS, hit_point):
                return False
	    # If m-line encountered and robot is closer to goal than hit point, track m-line
            if abs(BUG_POS[0]) < 2 and dist(BUG_POS, Q_GOAL) < dist(hit_point, Q_GOAL):
		# Debug output
                print("reached m-line")
		# Align robot onto m-line
		left_deg(90 - BUG_POS[2])
		sleep(0.3)
		servo(90)
		sleep(0.25)
		# If obstacle is in front of robot, continue following original obstacle
		if us_dist(15) < 15:
		    continue
		break

                
if __name__ == "__main__":
    enable_servo()
    servo(90)
    # Q_GOAL is given by user
    y_goal = int(raw_input("Enter goal y-coordinate: "))
    # Adjust for sensor inaccuracies, maintain robot's coord syst in scaled down cm consistent with sensors
    Q_GOAL = [0, y_goal / 1.3]
    if bug2(Q_GOAL):
        print("Goal found!")
    else:
        print("Impossible :(")
    draw_map()
