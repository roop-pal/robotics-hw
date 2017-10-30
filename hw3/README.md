This is a Lab 2 submission for group 24
Team Members: Jacques Van Anh(qv2106), Roop Pal(rmp2191), Yusuke Hayashi(yh2886)
Youtube link for color tracking demo: https://www.youtube.com/watch?v=FzAM3GcZ6_c
Adjustments to color tracking Algorithm:
- HSV color representation
- Rectangle chosen based on min_x, max_x, min_y, and max_y of points selected
- Mean is the average hue in said rectangle
- Threshold is between (mean - 10, 50, 50) and (mean + 10, 255, 255)
Assumptions Made:
 - The biggest area of the mask is the object to follow
 - The region is properly selected with the four points
