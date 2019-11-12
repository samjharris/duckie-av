import numpy as np

import positions
from odometry_guided_feedback import get_PWMs_from_odometry
from visual_controller import get_PWMs_from_visual
from ticks_to_distance import get_distances



x_act = np.array([0,0,0])
x_act_prev = np.array([0,0,0])
x_ref_func = positions.get_x_ref_func_one_meter()
PWM_l, PWM_r = 0, 0


def compute_motor_values(t, delta_t, left_encoder, right_encoder, delta_left_encoder, delta_right_encoder):
    global x_act
    global x_act_prev
    global x_ref_func
    global PWM_l, PWM_r


    # translate encoder values to distances and generate new PWMs
    dist_l, dist_r = get_distances(delta_left_encoder, delta_right_encoder)
    x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
    x_act = x_act_new

    # get displacement from center of the lane from visual components
    # TODO: call for this from visual processing module
    # lane_error, stop_marker = get_lane_error()
    lane_error, stop_marker = 0, False

    # compute the new motor commands
    # PWM_l, PWM_r = get_PWMs_from_odometry(x_ref_func, t, delta_t, x_act, x_act_prev, PWM_l, PWM_r)
    PWM_l, PWM_r = get_PWMs_from_visual(lane_error, delta_t, stop_marker, PWM_l, PWM_r)
    x_act_prev = x_act

    # debug
    print("x_ref_func(t): {}".format(x_ref_func(t)))
    print("x_act: {}".format(x_act))
    print("PWM_l: {}".format(PWM_l))
    print("PWM_r: {}".format(PWM_r))
    print("delta_left_encoder: {}".format(delta_left_encoder))
    print("delta_right_encoder: {}".format(delta_right_encoder))
    print("="*30)

    # send the new motor signals
    PWM_l, PWM_r = int(PWM_l), int(PWM_r)
    return PWM_l, PWM_r
