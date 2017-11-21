#Lab 4
###Group 24 [qv2106, rmp2191, yh2886]
###Youtube link: https://www.youtube.com/watch?v=DdURFlCAmps?vik

You can find our main in lane_follower.py.
We made the following assumptions about our robot/environment: 
- Colors/lighting fit hardcoded color thresholds for yellow and orange
- Track's blue dots are accurate for picking points for homography
- Lines are sufficiently straight

##Values calculated from ta_supplied_image_set:

calculated_angle_offset = -16.27 degrees

calculated_distance_offset = 144.203

homography_transform_matrix = 

[[ -1.00673524e+02  -1.27382827e+02   1.73857013e+04]
 
 [  5.49623552e+00  -4.83668726e+02   3.73194392e+04]
 
 [  2.70657879e-02  -7.99162850e-01   1.00000000e+00]]

distance_to_camera_from_homography = 13.5cm


##Values calculated from student_captured_image_set

calculated_angle_offset =  -76.96 degrees

calculated_distance_offset =  -28.13

homography_transform_matrix = 

[[  9.11029639e+00   8.21713008e+00  -1.05715165e+03]

 [ -2.32918087e-01   3.77327301e+01  -2.66691210e+03]
 
 [ -2.52054754e-03   5.80161563e-02   1.00000000e+00]]
 
distance_to_camera_from_homography = 31cm


##Questions:
1) The architecture is the same as given in the slides here: https://docs.google.com/presentation/d/1yHv466e0iReHPVEZLOzA6salj6OwyLRpTkvZBna598g/edit
2) The robot point was set to a distance behind the bottom of the original image, transformed via homography image, and it's x-coordinate was compared to the line's x-coordinate calculated by ρ * cos(Θ). 
3) The robot line's theta was compared to the hough line's theta.
4) If there is an orange blob above a minimum area, turn 180. If there are no lines, turn right. There are then 9 cases by the combination of angle offset being negative, positive, or below thresholds (equal) and dist offset being negative, positive, or below thresholds (equal). L means left, R means right, F means forward.
- Positive angle
 - Positive dist: LF
 - Negative dist: FL
 - Equal    dist: L
- Negative angle
 - Positive dist: FR
 - Negative dist: RF
 - Equal    dist: R
- Equal
 - Positive dist: LFR
 - Negative dist: RFL
 - Equal    dist: F
5) It defines the robot's position.
