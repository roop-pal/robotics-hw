import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

DIM = 600

def my_y(y):
    return DIM - y

def get_obstacles():
    f = open("world_obstacles.txt", 'r')
    
    segments = []
    num_obstacles = int(f.readline())
    for i in range(num_obstacles):
        num_vertices = int(f.readline())
        vertices = []
        for j in range(num_vertices):
            x,y = f.readline().split()
            vertices.append((int(x), my_y(int(y))))
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
    starty = my_y(int(startline[1]))
    endx = int(endline[0])
    endy = my_y(int(endline[1]))

    f.close()

    return [(startx, starty), (endx, endy)]


if __name__ == '__main__':
    distance = 5
    if len(sys.argv) > 1:
        distance = int(sys.argv[1])
    print "DISTANCE set as " + str(distance)

    segs = get_obstacles()
    endpoints = get_start_and_end()
    endpoints_x, endpoints_y = zip(*endpoints)
    plt.scatter(endpoints_x, endpoints_y, color='r')

    lc = mc.LineCollection(segs)

    ax = plt.axes()
    ax.add_collection(lc)
    ax.autoscale()
    
    plt.show()