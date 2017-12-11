import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import random
import math


DIM = 600
N = 200

class Node:
    def __init__(self, x, y, parent):
        self.xy = (x,y)
        self.x = x
        self.y = y
        self.parent = parent

def my_y(y):
    return DIM-y

def dist(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


def get_obstacles():
    f = open("world_obstacles.txt", 'r')
    
    segments = []
    num_obstacles = int(f.readline())
    for i in range(num_obstacles):
        num_vertices = int(f.readline())
        vertices = []
        for j in range(num_vertices):
            x,y = f.readline().split()
            #vertices.append((int(x), my_y(int(y))))
            vertices.append((int(x), int(y)))
        for j in range(1,num_vertices):
            v1 = vertices[j-1]
            v2 = vertices[j]
            segments.append([v1, v2])
        startv = vertices[0]
        endv = vertices[num_vertices-1]
        segments.append([endv, startv])

    f.close()
    return segments

def get_start_and_end():
    f = open("start_goal.txt", 'r')

    startline = f.readline().split()
    endline = f.readline().split()

    startx = int(startline[0])
    #starty = my_y(int(startline[1]))
    starty = int(startline[1])
    endx = int(endline[0])
    #endy = my_y(int(endline[1]))
    endy = int(endline[1])

    f.close()

    return [(startx, starty), (endx, endy)]


def update_plot(paths, q1, q2):
    plt.scatter(q1[0], q1[1], color='black', s=[10])
    segs = paths.get_segments()
    segs.append([q1, q2])
    paths.set_segments(segs)
    plt.pause(0.05)


def highlight_path(goal):
    currNode = goal
    path = []
    while currNode.parent != None:
        #plt.scatter(currNode.x, currNode.y, color='yellow', s=[10])
        path.append([currNode.xy, currNode.parent.xy])
        currNode = currNode.parent
        
    lc = mc.LineCollection(path, color='yellow')
    ax = plt.axes()
    ax.add_collection(lc)

def build_rrt(start, goal, step, paths, obstacles):
    root = Node(start[0], start[1], None)
    points_list = [root]

    while True:
        if random.random() <= 0.05:
            q_rand = goal
        else:
            q_rand = random.random()*DIM, random.random()*DIM

        q_new = extend_rrt(points_list, q_rand, step, obstacles, paths.get_segments())
        if q_new != None:
            points_list.append(q_new)
            update_plot(paths, q_new.xy, q_new.parent.xy)

            if dist(q_new.xy, goal) <= step:
                update_plot(paths, q_new.xy, goal)
                goal_node = Node(goal[0], goal[1], q_new)
                highlight_path(goal_node)
                break



def extend_rrt(points_list, q_rand, step, obstacles, paths):
    q_near = None
    minDist = DIM*2
    
    # find closest neighbor
    for q in points_list:
        d = dist(q.xy, q_rand)
        if d < minDist:
            minDist = d
            q_near = q
    #print 'q_near', q_near
    if dist(q_rand, q_near.xy) < step:
        return None

    dx = q_rand[0] - q_near.x
    dy = q_rand[1] - q_near.y
    mag = math.sqrt(math.pow(dx,2) + math.pow(dy,2))

    q_newx = q_near.x + step*dx/mag
    q_newy = q_near.y + step*dy/mag
    q_new = (q_newx, q_newy)
    #print 'q_new', q_new

    if check_collision(q_new, q_near.xy, obstacles, paths) == False:
        return Node(q_newx, q_newy, q_near)
    return None

    #return Node(q_newx, q_newy, q_near)
    

def orientation(a, b, c):
    if ((b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])) > 0:
        return 1
    return -1
        
def check_collision(q1, q2, obstacles, paths):
    borders = obstacles #+ paths
    for border in borders:
        b1 = border[0]
        b2 = border[1]
        if intersect(q1, q2, b1, b2):
            return True
    return False


def intersect(a, b, c, d):
    if orientation(a, c, d) == orientation(b, c, d):
        return False
    elif orientation(a, b, c) == orientation(a, b, d):
        return False
    return True


if __name__ == '__main__':
    distance = 5
    if len(sys.argv) > 1:
        distance = int(sys.argv[1])
    print "DISTANCE set as " + str(distance)

    obstacles = get_obstacles()
    endpoints = get_start_and_end()
    endpoints_x, endpoints_y = zip(*endpoints)
    plt.scatter(endpoints_x, endpoints_y, color='r')

    obstacles_lc = mc.LineCollection(obstacles, color='b')
    paths = mc.LineCollection([], color='black')

    ax = plt.axes()
    ax.add_collection(obstacles_lc)
    ax.add_collection(paths)
    ax.autoscale()
    plt.ion()
    plt.gca().invert_yaxis()

    build_rrt(endpoints[0], endpoints[1], distance, paths, obstacles)
    plt.ioff()
    plt.show()