# CICS 503 Fall 2019 DuckieTown Group 4
# config.py

#cm/s/PWM
CM_S_PWM = 0.15

# minimum PWM required to move the robot
MIN_PWM = 100.0 #prev min_pwm

# mass of the robot (kilograms)
ROBOT_MASS = 0.830 #

# yoke point distance from center of the wheel base (centimeters)
YOKE_POINT = 5.0 #prev r_length

# K of 0.5, B of 3 and I of 30 work well for straight
# K of 20.0, B of 0.0 work well for visual control
K = 70.0  # spring constant
B = 0.0  # damper constant
I = 5.0  # length of torque arm

DIST_TO_ROI_CM = 15.0 # distance from bot to center of ROI
# LANE_WIDTH_PIX = 131.0
LANE_WIDTH_PIX = 66.0 # based on experimental values
LANE_WIDTH_CM = 20.25
PIX_PER_CM = LANE_WIDTH_PIX / LANE_WIDTH_CM # pixels per cm in ROI

TIME_SLICE = 0.1 # fraction of a second; resolution of our function
END_GOAL = 100.0 # goal is one meter measured in centimeters
STRAIGHT_SPEED_LIMIT = 15.0 # cm/s
TURN_SPEED_LIMIT = 10.0 # cm/s

CIRCLE_RADIUS = 30.0

WHEEL_BASE = 16.5
# BAUDRATE = 9600
BAUDRATE = 115200

DEBUG_INFO_ON = False