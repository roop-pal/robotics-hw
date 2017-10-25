from gopigo import *
import time

# locating object within some distance threshold
def find_object(threshold):
	while us_dist(15) > threshold:
		print "turning. dist: ", us_dist(15)
		enc_tgt(1,1,1)
		right_rot()
		time.sleep(2)



enable_encoders()
enable_servo()
servo(90)
find_object(200)
count = 0
# object encountered, continue to scan rest of object to where it ends
while us_dist(15) <= 200:
	print "turning, dist: ", us_dist(15)
	enc_tgt(1, 1, 1)
	right_rot()
	count += 1
	time.sleep(2)

# turns towards the middle of where the object was first and last sensed
enc_tgt(1, 1, count / 2)
left_rot()
time.sleep(2)

# is ready now to move towards target
print "repositioning, dist: ", us_dist(15)


fwd()
# trim adjusted, but in case robot veers off straight or target moves, fail-safe below.
prevDist = us_dist(15)
while True:
	time.sleep(0.1)
	currDist = us_dist(15)
	print "dist: ", currDist
	# if robot loses site of target, look to find it again.
	if prevDist < currDist or currDist > 150:
		print "lost"
		stop()
		find_object(prevDist + 50)
		fwd()
	# if robot is at target, stop.
	if currDist <= 30:
		stop()
		print "stop, dist: ", currDist
		break
	prevDist = currDist

	
