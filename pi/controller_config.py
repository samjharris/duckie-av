# CICS 503 Fall 2019 DuckieTown Group 4
# controller_config.py


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
