# Odometry-Guided Feedback Controller
# translate and rotate to minimize the error between where the robot thinks it
# is and where it should be, i.e.:
# Fcontrol = -K((x,y)act - (x,y)ref) - B((x_vel,y_vel)act)
# map the Fcontrol to a PWM command for both wheels. Tune the values
# of K and B to make this work the way you want it to.
#
# Inputs:
#         x_ref(t)   = function taking time returning triple:
#                                                   [x_ref, y_ref, theta_ref]
#         x_act      = [x_act, y_act, theta_act]
#         t          = time, int
#         PWM_R_prev = voltage, scalar
#         PWM_L_prev = voltage, scalar
#
# Returns:
#         PWM_R_prev = voltage, scalar
#         PWM_L_prev = voltage, scalar


import numpy as np

def get_PWMs(x_ref_func, t, x_act, PWM_L_prev, PWM_R_prev):

    # mass of the robot
    m = 1

    # yoke point distance from center of the wheel base
    r_length = 1

    # I is some function of k and B
    I = 1

    x_ref = x_ref_func(t)

    # Direction from bot to x_ref
    F_pd = np.array([x_ref[0] - x_act[0], x_ref[1] - x_act[1]])

    # Unit vector in direction of x_act
    x_r = np.array([np.cos(np.deg2rad(x_act[2])), np.sin(np.deg2rad(x_act[2]))])

    # Should we include k here??
    delta_PWM_trans = np.dot(F_pd, x_r) / m

    # Cross product to get M_rot
    r = x_r * r_length
    M_rot = np.cross(r, F_pd)
    delta_PWM_rot = r_length * (M_rot / I)

    PWM_L_new = PWM_L_prev + delta_PWM_trans - delta_PWM_rot
    PWM_R_new = PWM_R_prev + delta_PWM_trans + delta_PWM_rot

    return (PWM_L_new, PWM_R_new)

def x_ref_dumb_func(t):
    return np.array([2,0,0])

def test():
    test_x_act = np.array([1,-1,-15])
    result = get_PWMs(x_ref_dumb_func, 1, test_x_act, 0, 0)
    print(result)

test()
