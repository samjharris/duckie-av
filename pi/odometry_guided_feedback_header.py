# CICS 503 Fall 2019 DuckieTown Group 4
# Odometry-Guided Feedback header

import numpy as np

cm_per_sec_per_PWM = 0.15
min_pwm = 70

# mass of the robot (kilograms)
m = 0.830

# yoke point distance from center of the wheel base (centimeters)
r_length = 5

K = -0.5  # spring constant
B = 0.8   # damper constant
I = 20    # 
