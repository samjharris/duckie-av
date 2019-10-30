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
def get_PWMs(x_ref_func, t, x_act, PWM_L_prev, PWM_R_prev):

    # TODO: measure this
    # mass of the robot (kilograms)
    m = 0.750

    # TODO: measure this
    # yoke point distance from center of the wheel base (centimeters)
    r_length = 0.5

    K = -1  # spring constant
    B = 0.1  # damper constant

    # TODO: check this formula
    # https://en.wikipedia.org/wiki/Moment_of_inertia
    I = m*r_length*r_length

    # The target in the world frame
    x_ref = x_ref_func(t)

    # Unit vector in direction of x_act
    x_unit_bot = np.array([np.cos(np.deg2rad(x_act[2])),
                           np.sin(np.deg2rad(x_act[2]))])

    # World Frame location of the yoke point
    x_r = x_unit_bot * r_length + x_act[:2]

    # Distance vector from yoke to x_ref
    x_spring = x_ref[0:2] - x_r
    spring_displacement = np.linalg.norm(x_spring)

    # Unit vector in direction from yoke to x_ref
    x_unit_spring = x_spring / spring_displacement

    # TODO correct to using x_act_prev - x_act / timeslice
    speed = (PWM_L_prev + PWM_R_prev) / 2

    world_frame_velocity = np.array([speed * x_unit_bot[0],
                                     speed * x_unit_bot[1]])
    spring_frame_velocity = np.dot(world_frame_velocity,
                                   x_unit_spring) * x_unit_spring
    spring_frame_speed = np.linalg.norm(spring_frame_velocity)

    # F_pd as given by the spring / damper function
    # F_pd = -K * x - B * x_dot
    F_pd = (-K * spring_displacement - B * spring_frame_speed) * x_unit_spring

    # F_trans = <F_pd, x_yoke_robot_frame>
    # F_trans / m = delta_PWM_trans
    r = x_unit_bot * r_length
    delta_PWM_trans = np.dot(F_pd, r) / m

    # M_rot = r cross F_pd
    # delta_theta_dot = M_rot / I = r cross F_pd
    # delta_PWM_rot = delta_theta_dot * r_length
    M_rot = np.cross(r, F_pd)
    delta_PWM_rot = r_length * (M_rot / I)

    # Add delta PWMs to previous values to obtain new values
    # Subtract rotational term from left and add to right (right hand rule)
    PWM_L_new = min(max(PWM_L_prev + delta_PWM_trans - delta_PWM_rot, -400), 400)
    PWM_R_new = min(max(PWM_R_prev + delta_PWM_trans + delta_PWM_rot, -400), 400)

    def print_debug_info():
        print("x_act")
        print(x_act)
        print("x_ref")
        print(x_ref)
        print("x_unit_bot")
        print(x_unit_bot)
        print("x_r")
        print(x_r)
        print("x_spring")
        print(x_spring)
        print("spring_displacement")
        print(spring_displacement)
        print("x_unit_spring")
        print(x_unit_spring)
        print("speed")
        print(speed)
        print("world_frame_velocity")
        print(world_frame_velocity)
        print("spring_frame_velocity")
        print(spring_frame_velocity)
        print("spring_frame_speed")
        print(spring_frame_speed)
        print("F_pd")
        print(F_pd)
        print("delta_PWM_trans")
        print(delta_PWM_trans)
        print("r")
        print(r)
        print("M_rot")
        print(M_rot)
        print("delta_PWM_rot")
        print(delta_PWM_rot)
        print("PWM_L_new")
        print(PWM_L_new)
        print("PWM_R_new")
        print(PWM_R_new)
    # print_debug_info()
    return (PWM_L_new, PWM_R_new)


def x_ref_dumb_func(t):
    return np.array([9,9,0])


def test():
    test_x_act = np.array([2,-2.0,15])
    result = get_PWMs(x_ref_dumb_func, 1, test_x_act, 10, 10)
    print(result)
