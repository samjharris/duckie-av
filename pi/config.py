# CICS 503 Fall 2019 DuckieTown Group 4
# config.py

#cm/s/PWM
CM_S_PWM = 0.15

# minimum PWM required to move the robot
MIN_PWM = 55 #prev min_pwm

# mass of the robot (kilograms)
ROBOT_MASS = 0.830 #

# yoke point distance from center of the wheel base (centimeters)
YOKE_POINT = 5 #prev r_length

# K of 0.5, B of 3 and I of 30 work well for straight
K = -0.6  # spring constant
B = 3  # damper constant
I = 5    # length of torque arm

TIME_SLICE = 0.1 # fraction of a second; resolution of our function
END_GOAL = 100 # goal is one meter measured in centimeters
STRAIGHT_SPEED_LIMIT = 15 # cm/s
TURN_SPEED_LIMIT = 10 # cm/s

CIRCLE_RADIUS = 30

WHEEL_BASE = 16.5
# BAUDRATE = 9600
BAUDRATE = 115200