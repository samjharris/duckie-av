# CICS 503 Fall 2019 DuckieTown Group 4
# controller_config.py
import numpy as np

#cm/s/PWM
CM_S_PWM = 0.15

# minimum PWM required to move the robot
MIN_PWM = 70 #prev min_pwm

# mass of the robot (kilograms)
ROBOT_MASS = 0.830 #

# yoke point distance from center of the wheel base (centimeters)
YOKE_POINT = 5 #prev r_length

K = -0.5  # spring constant
B = 0.8   # damper constant
I = 20    # length of torque arm

TIME_SLICE = 0.5 # fraction of a second; resolution of our function
END_GOAL = 100 # goal is one meter measured in centimeters
SPEED_LIMIT = 5 # cm/s
    
CIRCLE_RADIUS = 10

WHEEL_BASE = 16.5
BAUDRATE = 9600

