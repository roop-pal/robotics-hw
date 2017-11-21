#Lab 4
###Group 24 [qv2106, rmp2191, yh2886]
###Youtube link: https://www.youtube.com/watch?v=DdURFlCAmps?vik

You can find our main in lane_follower.py.
We made the following assumptions about our robot/environment: 
- Colors/lighting fit hardcoded color thresholds for yellow and orange
- Track's blue dots are accurate for picking points for homography
- Lines are sufficiently straight

##Values calculated from ta_supplied_image_set:
calculated_angle_offset = <angle_offset>
calculated_distance_offset = <distance_offset in cm>
homography_transform_matrix = <matrix>
distance_to_camera_from_homography = <distance in cm>

##Values calculated from student_captured_image_set
calculated_angle_offset =  -76.96 degrees
calculated_distance_offset =  -28.13
homography_transform_matrix = 
[[  9.11029639e+00   8.21713008e+00  -1.05715165e+03]
 [ -2.32918087e-01   3.77327301e+01  -2.66691210e+03]
 [ -2.52054754e-03   5.80161563e-02   1.00000000e+00]]
distance_to_camera_from_homography = 31

##Questions:
1) Describe the overall architecture of your implementation.
2) What method did your group use to calculate the distance from the center line?
3) What method did your group use to calculate the angle offset from the center line?
4) Describe your control flow algorithm based on distance, angle, and whatever other metrics you used.
5) What is the purpose of the distance offset from the camera to the homography transform?
