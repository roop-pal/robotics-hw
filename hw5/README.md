#Lab 5
###Group 24 [qv2106, rmp2191, yh2886]

You can find our main in rrt.py. This was written for Python2.7.

Our implementation specific details are:
* Collision detection is done by determining if a new segment-to-be-drawn intersects with any obstacle boundary. To determine an intersection, we compare the orientation of the four segment endpoints (2 endpoints of new segment + 2 endpoints of obstacle border).
* In addition to collision with obstacle boundaries, we avoid new segments colliding with the existing tree by treating the following as a collision: the randomly generated configuration (q_rand) and its nearest neighbor (q_near) are less than step-size from each other. This is because this scenario will cause the new segment to extend from q_near past q_rand, which may bring it closer to another node in the tree (i.e. q_near ceases to be the actual nearest neighbor)
* There is a 5% bias of choosing the goal point as the randomly generated point at each iteration. 
* The script will terminate following 1000000 consecutive iterations of non-collision-free generated configurations.  

Any special assumption we made are:
* The program will run for at most 10000000 iterations (an invalid q_rand due to collision still counts as 1 iteration).
* The dimensions of the world are 600x600. This is set as a global variable DIM. 

Images of sample results are stored in rrt.png and rrt-bi.png for non-bidirectional and bidirectional runs respectively.

The script expects command-line arguments in the following format:
'python rtt.py <distance> <obstacles-file> <start-goal-file> <-b>'

-b is an optional argument specifying the program to run bidirecitonal RRT. For example, to run the homework files with step size 20:
'python rtt.py 20 world_obstacles.txt start_goal.txt'
or
'python rtt.py 20 world_obstacles.txt start_goal.txt -b'
