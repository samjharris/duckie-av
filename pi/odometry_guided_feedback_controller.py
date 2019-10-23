# CICS 503 Fall 2019 DuckieTown Group 4
# Odometry-Guided Feedback Controller

import numpy as np


# Inputs:
#         x_ref(t)   = function taking time returning triple:
#                                                   [x_ref, y_ref, theta_ref]
#                      theta is expected in degrees, not radians
#         x_act      = [x_act, y_act, theta_act]
#         t          = time, int
#         PWM_R_prev = voltage, scalar
#         PWM_L_prev = voltage, scalar
#
# Returns:
#         (PWM_R_new, PWM_L_new) = pair of motor control signals in the range [-400, 400]
def get_PWMs(x_ref_func, t, x_act, PWM_L_prev, PWM_R_prev):

    # TODO: measure this
    # mass of the robot (kilograms)
    m = 1.0

    # TODO: measure this
    # yoke point distance from center of the wheel base (meters)
    r_length = 1.0

    K = 1  # spring constant
    B = 1  # damper constant

    # TODO: check this formula
    # https://en.wikipedia.org/wiki/Moment_of_inertia
    I = m*r_length*r_length

    # The target in the world frame
    x_ref = x_ref_func(t)

    # Unit vector in direction of x_act
    x_r = np.array([np.cos(np.deg2rad(x_act[2])), np.sin(np.deg2rad(x_act[2]))])

    # F_pd as given by the spring / damper function
    # F_pd = -K((x,y)act - (x,y)ref) - B((x_speed, y_speed)act)
    speed = (PWM_L_prev + PWM_R_prev) / 2
    world_frame_velocity = np.array([speed * x_r[0], speed * x_r[1]])
    F_pd = -K * (x_act[0:2] - x_ref[0:2]) - B * (world_frame_velocity)

    # F_trans = <F_pd, x_r> / m = delta_PWM_trans
    delta_PWM_trans = np.dot(F_pd, x_r) / m

    # M_rot = r cross F_pd
    # delta_theta_dot = M_rot / I = r cross F_pd
    # delta_PWM_rot = delta_theta_dot * r_length
    r = x_r * r_length
    M_rot = np.cross(r, F_pd)
    delta_PWM_rot = r_length * (M_rot / I)

    # Add delta PWMs to previous values to obtain new values
    # Subtract rotational term from left and add to right (right hand rule)
    PWM_L_new = PWM_L_prev + delta_PWM_trans - delta_PWM_rot
    PWM_R_new = PWM_R_prev + delta_PWM_trans + delta_PWM_rot

    return (PWM_L_new, PWM_R_new)


def x_ref_dumb_func(t):
    return np.array([2,0,0])


def test():
    test_x_act = np.array([1,-1,-15])
    result = get_PWMs(x_ref_dumb_func, 1, test_x_act, 0, 0)
    print(result)
