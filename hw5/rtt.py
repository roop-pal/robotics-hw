import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import random
import math

DIM = 600
N = 10000000

# Defines a node in the tree, with a reference to parent node
class Node:
    def __init__(self, x, y, parent):
        self.xy = (x,y)
        self.x = x
        self.y = y
        self.parent = parent


# Computes the Euclidean distance between 2 points
def dist(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


# Reads obstacle file and returns a list of segments defining the obstacle borders
# (segments are store as lists of 2 tuples, each defining a xy-coordinate)
def get_obstacles(obstacle_file):
    f = open(obstacle_file, 'r')
    
    segments = []
    num_obstacles = int(f.readline())
    for i in range(num_obstacles):
        num_vertices = int(f.readline())
        vertices = []
        for j in range(num_vertices):
            x,y = f.readline().split()
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


# Reads the start-goal file and returns the endpoints as a list of xy-coordinates
def get_start_and_end(start_goal_file):
    f = open(start_goal_file, 'r')

    startline = f.readline().split()
    endline = f.readline().split()

    startx = int(startline[0])
    starty = int(startline[1])
    endx = int(endline[0])
    endy = int(endline[1])

    f.close()

    return [(startx, starty), (endx, endy)]


# Given 2 new points, draw the segment between them on the plot
# color of the segment is determined by boolean fromStart
def update_plot(paths, q1, q2, fromStart):
    if fromStart:
        c = 'black'
    else:
        c = 'magenta'
    plt.scatter(q1[0], q1[1], color=c, s=[10])
    segs = paths.get_segments()
    segs.append([q1, q2])
    paths.set_segments(segs)
    plt.pause(0.05)


# Given the reached goal node, traverse back up to the root, 
# highlighting each segment path with a yellow color
def highlight_path(goal):
    currNode = goal
    path = []
    while currNode.parent != None:
        path.append([currNode.xy, currNode.parent.xy])
        currNode = currNode.parent
        
    lc = mc.LineCollection(path, color='yellow')
    ax = plt.axes()
    ax.add_collection(lc)


# Determine if rancomly generating configuration q_rand is collision-free
# Return a new node one step size away from q_rand's nearest neighbor if collision free
# Return None if not
def extend_rrt(points_list, q_rand, step, obstacles):
    q_near = None
    minDist = DIM*2
    
    # find closest neighbor
    for q in points_list:
        d = dist(q.xy, q_rand)
        if d < minDist:
            minDist = d
            q_near = q
    
    # return q_rand is too close to tree as extending by step size might cause collision with already-drawn segments
    if dist(q_rand, q_near.xy) < step:
        return None

    # find unit vector in direction q_near -> q_rand to compute q_new
    dx = q_rand[0] - q_near.x
    dy = q_rand[1] - q_near.y
    mag = math.sqrt(math.pow(dx,2) + math.pow(dy,2))

    q_newx = q_near.x + step*dx/mag
    q_newy = q_near.y + step*dy/mag
    q_new = (q_newx, q_newy)

    # check collision
    if check_collision(q_new, q_near.xy, obstacles) == False:
        return Node(q_newx, q_newy, q_near)
    return None


# Build unidirectional RRT
def build_rrt(start, goal, step, paths, obstacles):
    root = Node(start[0], start[1], None)
    points_list = [root] #list of nodes
    consecutive_none = 0 #keep track of consecutive unsuccessful iterations

    for i in range(N):
        # Bias of 5% of choosing goal node as q_rand
        if random.random() <= 0.05:
            q_rand = goal
        else:
            q_rand = random.random()*DIM, random.random()*DIM

        q_new = extend_rrt(points_list, q_rand, step, obstacles)

        # if new node is collision-free, extend the tree
        if q_new != None:
            points_list.append(q_new)
            update_plot(paths, q_new.xy, q_new.parent.xy, True)

            # check if within step size of goal
            if dist(q_new.xy, goal) <= step:
                if check_collision(q_new.xy, goal, obstacles) == False:
                    update_plot(paths, q_new.xy, goal, True)
                    goal_node = Node(goal[0], goal[1], q_new)
                    highlight_path(goal_node)
                    break
            consecutive_none = 0

        # Exit if too many consecutive collisions
        else:
            consecutive_none += 1
            if consecutive_none > 0.1*N:
                print "No solution found"
                break


# Build bidirectional RRT
def build_bi_rrt(start, goal, step, paths_start, paths_goal, obstacles):
    root_start = Node(start[0], start[1], None)
    root_goal = Node(goal[0], goal[1], None)
    start_points_list = [root_start] # list of nodes in tree rooted at start
    goal_points_list = [root_goal] # list of nodes in tree rooted at goal

    fromStart = True # true if current iteration builds from true start node
    consecutive_none = 0 #keep track of consecutive unsuccessful iterations

    for i in range(N):
        # set appropriate goal node depending on iteration
        if fromStart:
            currGoal = goal
            goals_list = goal_points_list
            points_list = start_points_list
            p = paths_start
        else:
            currGoal = start
            goals_list = start_points_list
            points_list = goal_points_list
            p = paths_goal

        # Bias of 5% of choosing goal node as q_rand
        if random.random() <= 0.05:
            q_rand = currGoal
        else:
            q_rand = random.random()*DIM, random.random()*DIM

        q_new = extend_rrt(points_list, q_rand, step, obstacles)

        # if new node is collision-free, extend the tree        
        if q_new != None:
            points_list.append(q_new)
            update_plot(p, q_new.xy, q_new.parent.xy, fromStart)

            # check if new node is within step size of any node in opposite tree
            found_goal = False
            for g in goals_list:
                if dist(q_new.xy, g.xy) <= step:
                    if check_collision(q_new.xy, g.xy, obstacles) == False:
                        update_plot(p, q_new.xy, g.xy, fromStart)
                        goal_node = Node(g.x, g.y, q_new)
                        highlight_path(goal_node)
                        highlight_path(g)
                        found_goal = True
                        break
            if found_goal:
                break
            fromStart = not fromStart
            consecutive_none = 0

        # Exit if too many consecutive collisions
        else:
            consecutive_none += 1
            if consecutive_none > 0.1*N:
                print "No solution found"
                break


# Check if new segment q1-q2 would intersect with any obstacle border
def check_collision(q1, q2, obstacles):
    borders = obstacles
    for border in borders:
        b1 = border[0]
        b2 = border[1]
        if intersect(q1, q2, b1, b2):
            return True
    return False


# Determine orientation of three points (i.e. clockwise or counterclockwise)
def orientation(a, b, c):
    if ((b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])) > 0:
        return 1
    return -1


# Determine if segment a-b intersercts with segment c-d by compraing orientations
def intersect(a, b, c, d):
    if orientation(a, c, d) == orientation(b, c, d):
        return False
    elif orientation(a, b, c) == orientation(a, b, d):
        return False
    return True


if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print "Invalid number of arguments. Usage: python rtt.py <distance> <obstacles-file> <start-goal-file> <-b>"
        sys.exit(1)

    if len(sys.argv) == 5 and sys.argv[4] != '-b':
        print "Invalid argument"
        sys.exit(1)

    distance = int(sys.argv[1])
    print "DISTANCE set as " + str(distance)

    # Read in obstacles and plot world
    obstacles = get_obstacles(sys.argv[2])
    endpoints = get_start_and_end(sys.argv[3])
    endpoints_x, endpoints_y = zip(*endpoints)
    plt.scatter(endpoints_x, endpoints_y, color='r')
    obstacles_lc = mc.LineCollection(obstacles, color='b')
    paths_start = mc.LineCollection([], color='black')
    paths_goal = mc.LineCollection([], color='magenta')

    ax = plt.axes()
    ax.add_collection(obstacles_lc)
    ax.add_collection(paths_start)
    ax.add_collection(paths_goal)
    ax.autoscale()
    plt.ion()
    plt.gca().invert_yaxis()

    # Run RTT and save output
    if len(sys.argv) == 5:
        build_bi_rrt(endpoints[0], endpoints[1], distance, paths_start, paths_goal, obstacles)
        plt.ioff()
        plt.savefig('rtt-bi.png')
    else:
        build_rrt(endpoints[0], endpoints[1], distance, paths_start, obstacles)
        plt.ioff()
        plt.savefig('rtt.png')

    plt.show()
