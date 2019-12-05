# CICS 503 Fall 2019 DuckieTown Group 4
#
# config.py
# useful global variables are declared here
import numpy as np

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
# K = 3.0  # spring constant
K = 1.85  # spring constant
B = 0.00  # damper constant
I = 5.0  # length of torque arm
THETA_VEL_WINDOW = 2
ENCODER_VEL_WINDOW = 100
# ENCODER_VEL_WINDOW = 30

# Open Loop Intersection Distances
DIST_FROM_STOP_LINE = 30
STRAIGHT_DIST = DIST_FROM_STOP_LINE + 44
LEFT_TURN_DIST = DIST_FROM_STOP_LINE + 26

DIST_TO_ROI_CM = 15.0 # distance from bot to center of ROI
# LANE_WIDTH_PIX = 131.0
LANE_WIDTH_PIX = 55.0 # based on experimental values
LANE_WIDTH_CM = 20.25
PIX_PER_CM = LANE_WIDTH_PIX / LANE_WIDTH_CM # pixels per cm in ROI
WHITE_OFFSET_PIX = 20
YELLOW_OFFSET_PIX = 30

STRIP_LOCATION = 6

TIME_SLICE = 0.1 # fraction of a second; resolution of our function
END_GOAL = 100.0 # goal is one meter measured in centimeters

# STRAIGHT_SPEED_LIMIT_FAST = 15.9 # cm/s
# STRAIGHT_SPEED_LIMIT_SLOW = 11.1 # cm/s
STRAIGHT_SPEED_LIMIT_FAST = 14.2 # cm/s
STRAIGHT_SPEED_LIMIT_SLOW = 9.5 # cm/s
STRAIGHT_SPEED_LIMIT = STRAIGHT_SPEED_LIMIT_SLOW

TURN_SPEED_LIMIT = 10.0 # cm/s

CIRCLE_RADIUS = 30.0

CM_PER_TICK = 22.0/26.0

WHEEL_BASE = 16.5
QUARTER_TURN = WHEEL_BASE * np.pi / 4
# BAUDRATE = 9600
BAUDRATE = 115200

DEBUG_INFO_ON = False

TURN_DIRECTION = "right"

SAW_GREEN = True

# CONTROLLER ENUMS
HUG_WHITE = 0
HUG_YELLOW = 1
CONTROL_VISUAL = 0
CONTROL_OPEN = 1
CONTROL_STOP = 2
TURN_L = 0
TURN_R = 1
TURN_S = 2