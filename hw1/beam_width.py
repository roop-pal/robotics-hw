from gopigo import *
import time

sleep_time = 2

theta = 90
enable_servo()
servo(theta)
time.sleep(sleep_time)

dist = us_dist(15)
currDist = dist

# sweep left from 90 until sensor has large percentage increase in distance compared to last measurement
print "left sweep"
while (currDist - dist) * 1.0 / dist < 0.15:
	# debug code
	print "theta: ", theta, ", currDist: ", currDist, ", %: ",  (abs(currDist - dist) * 1.0 / dist)
	servo(theta)
	theta += 1
	time.sleep(sleep_time)
	currDist = us_dist(15)

print "theta: ", theta, ", currDist: ", currDist, ", %: ",  (abs(currDist - dist) * 1.0 / dist)

# sweep right from 90 until sensor has large percentage increase in distance compared to last measurement
left_theta = theta	
print "right sweep"
theta = 90
currDist = dist
while (currDist - dist) * 1.0 / dist < 0.15:
	# debug code
	print "theta: ", theta, ", currDist: ", currDist, ", %: ",  (abs(currDist - dist) * 1.0 / dist)
	servo(theta)
	theta -= 1
	time.sleep(sleep_time)
	currDist = us_dist(15)

print "theta: ", theta, ", currDist: ", currDist, ", %: ",  (abs(currDist - dist) * 1.0 / dist)

right_theta = theta


# print final beam width
print("Angle is", left_theta - right_theta)