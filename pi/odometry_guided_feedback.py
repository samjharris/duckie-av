# CICS 503 Fall 2019 DuckieTown Group 4
# Odometry-Guided Feedback

from config import *
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
def convert_vel_to_PWM(velocity):
    if(velocity > 0):
        # positive function: VELOCITY = 0.1305(PWM) - 11.649, x-intercept =89.2644
        return (velocity - 11.649) / 0.1305
    elif(velocity < 0):
        # negative function: VELOCITY = 0.1238(PWM) + 10.545, x-intercept =-85.177
        return (velocity + 10.545) / 0.1238
    else:
        return 0

def convert_PWM_to_vel(PWM):
    if PWM >  -MIN_PWM and PWM < MIN_PWM:
        #this is the deadzone, so the velocity should be 0
        return 0
    elif(PWM > 0):
        # positive function: VELOCITY = 0.1305(PWM) - 11.649, x-intercept =89.2644
        return (0.1305 * PWM) - 11.649
    else: #PWM < 0
        # negative function: VELOCITY = 0.1238(PWM) + 10.545, x-intercept =-85.177
        return (0.1238 * PWM) + 10.545

def convert_delta_PWM_to_vel(delta_PWM):
    if delta_PWM > 0:
        delta_PWM += MIN_PWM
    if delta_PWM < 0:
        delta_PWM -= MIN_PWM
    return convert_PWM_to_vel(delta_PWM)

def get_PWMs_from_odometry(x_ref_func, t, dt, x_act, x_act_prev, PWM_L_prev, PWM_R_prev):

    # Unit vector in direction of x_act
    x_unit_bot = np.array([np.cos(np.deg2rad(x_act[2])),
                           np.sin(np.deg2rad(x_act[2]))])

    # World  frame yoke vector
    r = x_unit_bot * YOKE_POINT

    # World Frame location of the yoke point
    x_r = r + x_act[:2]

    # The target in the world frame
    x_ref_yoke = x_ref_func(t)[:2] + r

    # Distance vector from yoke to x_ref_yoke
    x_spring = x_ref_yoke[0:2] - x_r

    delta_x_act = x_act_prev - x_act

    sign = 0
    dir_vel_vec = np.dot(x_spring, delta_x_act[:2])
    if(np.linalg.norm(dir_vel_vec) == 0):
        sign = 1
    else:
        dir_sign_vec = x_spring / dir_vel_vec
        # if the sign of the spring displacement is positive:
        if(dir_sign_vec[0] < 0):
            sign = 1
        # if the sign of the spring displacement is negative:
        elif(dir_sign_vec[0] > 0):
            sign = -1
        # if x_spring was 0:
        else:
            sign = 1

    spring_displacement = np.linalg.norm(x_spring)

    if spring_displacement == 0:
        return (PWM_L_prev, PWM_R_prev)
    # Unit vector in direction from yoke to x_ref_yoke
    x_unit_spring = x_spring / spring_displacement

    # TODO correct to using x_act_prev - x_act / timeslice
    #speed = (PWM_L_prev + PWM_R_prev) / 2

    spring_frame_vel = np.dot(delta_x_act[:2], np.array(x_unit_spring))
    norm = np.linalg.norm(spring_frame_vel)
    speed = norm / dt

    # F_pd as given by the spring / damper function
    # F_pd = -K * x - B * x_dot
    spring_component = -K * spring_displacement
    damping_component = B * speed
    F_pd = (spring_component - damping_component) * x_unit_spring

    # F_trans = <F_pd, x_yoke_robot_frame>
    # F_trans / m = delta_PWM_trans
    r = x_unit_bot * YOKE_POINT
    F_trans = sign * np.dot(F_pd, x_unit_bot)
    delta_vel_trans = (F_trans / ROBOT_MASS) 

    # M_rot = r cross F_pd
    # delta_theta_dot = M_rot / I = r cross F_pd
    # delta_PWM_rot = delta_theta_dot * YOKE_POINT
    M_rot = np.cross(r, F_pd)
    delta_vel_rot = YOKE_POINT * M_rot / I

    vel_L_new = speed + delta_vel_trans - delta_vel_rot
    vel_R_new = speed + delta_vel_trans + delta_vel_rot

    # Add delta PWMs to previous values to obtain new values
    # Subtract rotational term from left and add to right (right hand rule)

    max_vel_allowed = convert_PWM_to_vel(400)
    max_of_vel_news = max(abs(vel_L_new), abs(vel_R_new))

    # Added coefficient so that I could print the non-limited velocity goals
    velocity_reduction_coefficient = 1
    if max_of_vel_news > max_vel_allowed:
        velocity_reduction_coefficient = max_vel_allowed / max_of_vel_news

    PWM_L_new = int(convert_vel_to_PWM(velocity_reduction_coefficient * vel_L_new))
    PWM_R_new = int(convert_vel_to_PWM(velocity_reduction_coefficient * vel_R_new))

    def print_debug_info():
        np.set_printoptions(precision=3)
        # print("{:>22} : {}".format("K", K))
        # print("{:>22} : {}".format("B", B))
        print("{:>22} : {}".format("t", t))
        print("{:>22} : {}".format("x_act", x_act))
        # print("{:>22} : {}".format("PWM_L_prev", PWM_L_prev))
        # print("{:>22} : {}".format("PWM_R_prev", PWM_R_prev))
        # print("{:>22} : {}".format("x_unit_bot", x_unit_bot))
        # print("{:>22} : {}".format("x_r", x_r))
        # print("{:>22} : {}".format("x_ref_yoke", x_ref_yoke))
        # print("{:>22} : {}".format("x_spring", x_spring))
        # print("{:>22} : {}".format("dir_vel_vec", dir_vel_vec))
        # print("{:>22} : {}".format("delta_x_act", delta_x_act))
        # print("{:>22} : {}".format("spring_displacement", spring_displacement))
        # print("{:>22} : {}".format("x_unit_spring", x_unit_spring))
        # print("{:>22} : {}".format("norm", norm))
        # print("{:>22} : {}".format("dt", dt))
        # print("{:>22} : {}".format("speed", speed))
        # print("{:>22} : {}".format("spring_component", spring_component))
        # print("{:>22} : {}".format("damping_component", damping_component))
        # print("{:>22} : {}".format("F_pd", F_pd))
        # print("{:>22} : {}".format("delta_vel_trans", delta_vel_trans))
        # print("{:>22} : {}".format("r", r))
        # print("{:>22} : {}".format("F_trans", F_trans))
        # print("{:>22} : {}".format("M_rot", M_rot))
        # print("{:>22} : {}".format("delta_vel_rot", delta_vel_rot))
        # print("{:>22} : {}".format("vel_L_prev", vel_L_prev))
        # print("{:>22} : {}".format("vel_R_prev", vel_R_prev))
        # print("{:>22} : {}".format("vel_L_new", vel_L_new))
        # print("{:>22} : {}".format("vel_R_new", vel_R_new))
        # print("{:>22} : {}".format("max_vel_allowed", max_vel_allowed))
        # print("{:>22} : {}".format("PWM_L_new", PWM_L_new))
        # print("{:>22} : {}".format("PWM_R_new", PWM_R_new))
        # print("="*50)
    # print_debug_info()
    return (PWM_L_new, PWM_R_new)


def test(PWM_L, PWM_R, x_ref_x_val):
    def x_ref_dumb_func(t):
        return np.array([x_ref_x_val,0,0])

    test_x_act = np.array([0,0,0])
    result = get_PWMs(x_ref_dumb_func, 1, 1, test_x_act, test_x_act, 80, 80)
    print(result)
