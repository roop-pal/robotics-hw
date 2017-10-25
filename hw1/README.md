This is a Lab 1 submission for group 24 Team Members: Jacques Van Anh(qv2106), Roop Pal(rmp2191), Yusuke Hayashi(yh2886)

Question 1: Done. 

Question 2: Code implementation is found in dancing.py. During 20 seconds, for each second, the robot randomly chooses one of the following actions to execute: go forward, turn left, turn right, go backward, stop, increase speed, decrease speed.

Question 3: Code implementation is found in sensor_accuracy.py. 
Real: 5cm, recorded: 5cm
Real: 30cm, recorded: 36cm 
Real: 60cm, recorded: 78cm

Question 4: Code implementation is found in beam_width.py.
The beam width was found to be approximately 62 degrees.
Method description: The robot should be placed facing a long straight wall (about 20cm away). The servo will initially be set to 90 degrees and measure the distance found. The servo will be continually rotated one degree to the left, measuring the distance each time and comparing it to the initial distance. If the percentage difference between the two measurements is greater than 15% (emperically determined threshold), the servo will stop rotating and take the current degree orientation as the beam width for the left side. The servo is returned to 90 degrees and the entire process is rotated to the right. The total beam width is the sum of the value returned from both left and right sweeps.

Question 5: Code implementation is found in locate_object.py.
Method description: The initially starts rotating incrementally to the right while it senses a distance greater than 200cm. When the distance falls below 200, it has found the object, but keeps on rotating until the distance falls back up to above 200, keeping track of how many increments it has turned. The robot then repositions itself to the midpoint between when it first and last senses the object. This is to account for the large beam width so that the robot ends up facing the object center. It then moves forward towards the object, stopping when it senses a distance less than 30cm (accounting for error measuring 20cm). While moving forward, the robot may recalculate its trajectory if the distance it senses either increases or exceeds 150cm. 
