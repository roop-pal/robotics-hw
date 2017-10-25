from gopigo import *
import time

enable_servo()
servo(90)
time.sleep(3)

print us_dist(15), "cm"
