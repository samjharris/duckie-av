# CICS 503 Fall 2019 DuckieTown Group 4
# Closed loop controller
# Pseudocode:
# initialize x_act, PWM_L, PWM_R, time to zeros
# get path function
# in a loop
#     give all these to closed loop control function and get back new PWMs
#     give PWMs to arduino
#     wait for timeslice time
#     get left and right distance deltas from arduino
#     update x_act

import numpy as pd
import time
import positions
from  odometry_guided_feedback_controller import get_PWMs

timeslice = .25
x_act = [0,0,0]
PWM_L, PWM_R, time = 0, 0, 0
x_ref = positions.get_x_ref_func_one_meter()

while true:
    PWM_L, PWM_R = get_PWMs(x_ref, time, PWM_L, PWM_R)
    # send to PWMs to Arduino
    time.sleep(timeslice)
    # wait for input from Arduino: wheel distances as dist_l and dist_r
    x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
    if x_act == x_act_new:
        print("Route complete")
        break
    else:
        x_act = x_act_new
