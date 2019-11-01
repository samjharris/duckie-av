# CICS 503 Fall 2019 DuckieTown Group 4
# Odometry-Guided Feedback

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
#         (PWM_R_new, PWM_L_new) =
#                         pair of motor control signals in the range [-400, 400]
def get_PWMs(x_ref_func, t, dt, x_act, x_act_prev, PWM_L_prev, PWM_R_prev):

    cm_per_sec_per_PWM = 0.15
    min_pwm = 70
    def convert_vel_to_PWM(velocity):
        if velocity > 0:
            return min_pwm + velocity * cm_per_sec_per_PWM
        elif velocity < 0:
            return -min_pwm + velocity * cm_per_sec_per_PWM
        else:
            return 0


    def convert_PWM_to_vel(PWM):
        if PWM > 0:
            return (PWM - min_pwm) / cm_per_sec_per_PWM
        elif PWM < 0:
            return (PWM + min_pwm) / cm_per_sec_per_PWM
        else:
            return 0


    # mass of the robot (kilograms)
    m = 0.830

    # TODO: measure this
    # yoke point distance from center of the wheel base (centimeters)
    r_length = 5

    K = -0.5  # spring constant
    B = 0.8  # damper constant
    I = 20

    # Unit vector in direction of x_act
    x_unit_bot = np.array([np.cos(np.deg2rad(x_act[2])),
                           np.sin(np.deg2rad(x_act[2]))])

    # World  frame yoke vector
    r = x_unit_bot * r_length

    # World Frame location of the yoke point
    x_r = r + x_act[:2]

    # The target in the world frame
    x_ref = x_ref_func(t)[:2] + r

    # Distance vector from yoke to x_ref
    x_spring = x_ref[0:2] - x_r
    spring_displacement = np.linalg.norm(x_spring)

    # Unit vector in direction from yoke to x_ref
    x_unit_spring = x_spring / spring_displacement

    # TODO correct to using x_act_prev - x_act / timeslice
    #speed = (PWM_L_prev + PWM_R_prev) / 2
    delta_x_act = x_act_prev - x_act
    dot = np.dot(delta_x_act[:2], np.array(x_unit_spring))
    norm = np.linalg.norm(dot)
    speed = norm / dt

    # F_pd as given by the spring / damper function
    # F_pd = -K * x - B * x_dot
    F_pd = (-K * spring_displacement - B * speed) * x_unit_spring

    # F_trans = <F_pd, x_yoke_robot_frame>
    # F_trans / m = delta_PWM_trans
    r = x_unit_bot * r_length
    delta_vel_trans = np.dot(F_pd, r) / m

    # M_rot = r cross F_pd
    # delta_theta_dot = M_rot / I = r cross F_pd
    # delta_PWM_rot = delta_theta_dot * r_length
    M_rot = np.cross(r, F_pd)
    delta_vel_rot = r_length * M_rot / I

    vel_L_prev = convert_PWM_to_vel(PWM_L_prev)
    vel_R_prev = convert_PWM_to_vel(PWM_R_prev)

    vel_L_new = vel_L_prev + delta_vel_trans - delta_vel_rot
    vel_R_new = vel_R_prev + delta_vel_trans + delta_vel_rot

    # Add delta PWMs to previous values to obtain new values
    # Subtract rotational term from left and add to right (right hand rule)
    PWM_L_new = convert_vel_to_PWM(vel_L_new)
    PWM_R_new = convert_vel_to_PWM(vel_R_new)

    # print("{:>22} : {}".format("PWM_L_new before scaling", PWM_L_new))
    # print("{:>22} : {}".format("PWM_R_new before scaling", PWM_R_new))

    reduction_coefficient = 1
    if abs(PWM_L_new) > 400:
        reduction_coefficient = 400/abs(PWM_L_new)
    if abs(PWM_R_new) > 400:
        right_reduction_coefficient = 400/abs(PWM_R_new)
        reduction_coefficient = min(right_reduction_coefficient, reduction_coefficient)

    PWM_L_new = int(reduction_coefficient * PWM_L_new)
    PWM_R_new = int(reduction_coefficient * PWM_R_new)

    # print("{:>22} : {}".format("PWM_L_new after scaling", PWM_L_new))
    # print("{:>22} : {}".format("PWM_R_new after scaling", PWM_R_new))

    def print_debug_info():
        print("{:>22} : {}".format("x_act", x_act))
        print("{:>22} : {}".format("x_ref", x_ref))
        print("{:>22} : {}".format("PWM_L_prev", PWM_L_prev))
        print("{:>22} : {}".format("PWM_R_prev", PWM_R_prev))
        print("{:>22} : {}".format("x_unit_bot", x_unit_bot))
        print("{:>22} : {}".format("x_r", x_r))
        print("{:>22} : {}".format("x_spring", x_spring))
        print("{:>22} : {}".format("spring_displacement", spring_displacement))
        print("{:>22} : {}".format("x_unit_spring", x_unit_spring))
        print("{:>22} : {}".format("speed", speed))
        print("{:>22} : {}".format("F_pd", F_pd))
        print("{:>22} : {}".format("delta_vel_trans", delta_vel_trans))
        print("{:>22} : {}".format("r", r))
        print("{:>22} : {}".format("M_rot", M_rot))
        print("{:>22} : {}".format("delta_vel_rot", delta_vel_rot))
        print("{:>22} : {}".format("vel_L_prev", vel_L_prev))
        print("{:>22} : {}".format("vel_R_prev", vel_R_prev))
        print("{:>22} : {}".format("vel_L_new", vel_L_new))
        print("{:>22} : {}".format("vel_R_new", vel_R_new))
        print("{:>22} : {}".format("PWM_L_new", PWM_L_new))
        print("{:>22} : {}".format("PWM_R_new", PWM_R_new))
        print("="*30)
    print_debug_info()
    return (PWM_L_new, PWM_R_new)


def test(PWM_L, PWM_R):
    def x_ref_dumb_func(t):
        return np.array([9,0,0])

    test_x_act = np.array([0,0,0])
    result = get_PWMs(x_ref_dumb_func, 1, 1, test_x_act, test_x_act, 80, 80)
    print(result)
