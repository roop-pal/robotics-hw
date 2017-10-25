from gopigo import *
from time import *
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import *

threesixty = 30.0
WHEEL_RAD = 3.25

BUG_POS = [0, 0, 90, 0] # x, y, theta
MAP = [BUG_POS]
#q_goal = [0, 100]

def left_deg(deg):
    if deg < 0:
        right_deg(-deg)
        return
    BUG_POS[2] += deg
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        left_rot()
    stop()

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

def fwd_cm(dist):
    BUG_POS[0] += dist * math.cos(math.radians(BUG_POS[2]))
    BUG_POS[1] += dist * math.sin(math.radians(BUG_POS[2]))
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, cm2pulse(dist))
    while read_enc_status():
        fwd()
    stop()

def cm2pulse(dist):
    return int(dist / (2 * math.pi * WHEEL_RAD) * 18)


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def isatpoint(p1, p2):
    if dist(p1, p2) < 3:
        return True
    return False

def draw_map():
    print(len(MAP))
    x, y, u, v, colors = [], [], [], [], []
    for i in MAP:
        x.append(i[0])
        y.append(i[1])
        u.append(math.cos(math.radians(i[2])))
        v.append(math.sin(math.radians(i[2])))
        if i[3]:
            colors.append((1, 0, 0))
        else:
            colors.append((0, 0, 1))
    plt.figure()
    print(colors)
    ax = plt.gca()
    ax.quiver(x, y, u, v, colors)
    plt.draw()
    plt.show()

def bug2(q_goal):
    while True:
        while (us_dist(15) > 10):
            fwd_cm(5)
            sleep(0.2)
            if isatpoint(BUG_POS, q_goal):
                return True
        BUG_POS[3] = 1
        left_deg(90)
        BUG_POS[3] = 0
        hit_point = list(BUG_POS)

        while True:
            servo(0)
            sleep(0.2)
            right = us_dist(15)
            servo(90)
            sleep(0.2)
            forward = us_dist(15)
            # right sensor and fwd sensor tests
            if right < 10:
                BUG_POS[3] = 1
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
            if not right < 25:
                servo(45)
                sleep(0.2)
                if us_dist(15) < 25:
                    BUG_POS[3] = 1
                    left_deg(30)
                    sleep(0.25)
                    fwd_cm(3)
                    sleep(0.25)
                else:
                    fwd_cm(3)
                    sleep(0.25)
                    right_deg(30)
                    sleep(0.25)
            elif forward < 25:
                BUG_POS[3] = 1
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
            else:
                BUG_POS[3] = 1
                fwd_cm(5)
                sleep(0.25)
            # do move following bound
            print BUG_POS
            BUG_POS[3] = 0

            if dist(BUG_POS, q_goal) < 7:
                return True
            if isatpoint(BUG_POS, hit_point):
                return False
            if abs(BUG_POS[0]) < 2 and dist(BUG_POS, q_goal) < dist(hit_point, q_goal):
                print("reached mline")
                left_deg(90 - BUG_POS[2])
                sleep(0.3)
                servo(90)
                sleep(0.25)
                if us_dist(15) < 15:
                    continue
                break


if __name__ == "__main__":
    enable_servo()
    servo(90)

    xgoal = int(raw_input("Enter goal x-coordinate: "))
    ygoal = int(raw_input("Enter goal y-coordinate: "))
    q_goal = [xgoal, ygoal]

    if bug2(q_goal):
        print("Goal found!")
    else:
        print("Impossible :(")
    draw_map()
