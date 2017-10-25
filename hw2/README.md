This is a Lab 2 submission for group 24

Team Members: Jacques Van Anh(qv2106), Roop Pal(rmp2191), Yusuke Hayashi(yh2886)

Youtube link for bug2 demo: https://youtu.be/Qz2fo7h9yhY

Adjustments to Bug2 Algorithm:
- left-leaning
- m-line is always x = 0
- only last hit-point stored

Assumptions Made:
 - sensor readings are 1.3 * reality (sensor reads 30 cm when robot is 23 cm away from object)
     - robot coordinate system is based of sensor readings, not reality. e.g. fwd_cm(5) moves the robot ~3.85 cm forward.
     - q_goal is downscaled by 1.3 to fit this coordinate system
 - objects do not have gaps that cannot be sensed by robot
 - robot starts out facing goal
 - calibration constants (threesixty) are based of empirical data, changes rotation accuracy from robot to robot and environment to environment
 
 Description of Obstacle Boundary Following Algorithm
 - Front (90°) and right (0°) sensor readings are taken
 - In certain cases, front-right diagonal (45°) sensor reading is taken
 - Based on these readings, movement is determined. Specifics in code.
