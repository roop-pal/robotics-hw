from gopigo import *
import sys
import random

t_end = time.time() + 20

while time.time() < t_end:
	r = random.randint(1,7)

	if r==1:
		fwd()	# Move forward
	elif r==2:
		left()	# Turn left
	elif r==3:
		right()	# Turn Right
	elif r==4:
		bwd()	# Move back
	elif r==5:
		stop()	# Stop
	elif r==6:
		increase_speed()	# Increase speed
	elif r==7:
		decrease_speed()	# Decrease speed
	else:
		print "Something is wrong"
		
	time.sleep(1)

stop()
sys.exit()

