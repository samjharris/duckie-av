# CICS 503 Fall 2019 DuckieTown Group 4
#
# visual_control.py:
# provides visual control using the equation
# theta_2 = -K (theta - theta_ref) - B (theta_dot - theta_1_ref)
# theta_dot = theta_(t+1) - theta_t

from config import *
import numpy as np
from collections import deque
from time import sleep
from camera import Camera

sleep(2)

cam = Camera()

adjusted_speed = 0

previous_encoders = deque()
previous_encoder_dts = deque()

previous_thetas = deque()
previous_theta_dts = deque()

stopping = False
# pwm_total = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT) + convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)

def convert_vel_to_PWM(velocity):
    if(velocity > 0):
        # positive function: VELOCITY = 0.1305(PWM) - 11.649, x-intercept =89.2644
        return (velocity + 11.649) / 0.1305
    elif(velocity < 0):
        # negative function: VELOCITY = 0.1238(PWM) + 10.545, x-intercept =-85.177
        return (velocity - 10.545) / 0.1238
    else:
        return 0

def convert_PWM_to_vel(PWM):
    if PWM > -MIN_PWM and PWM < MIN_PWM:
        #this is the deadzone, so the velocity should be 0
        return 0
    elif(PWM > 0):
        # positive function: VELOCITY = 0.1305(PWM) - 11.649, x-intercept =89.2644
        return (0.1305 * PWM) - 11.649
    else: #PWM < 0
        # negative function: VELOCITY = 0.1238(PWM) + 10.545, x-intercept =-85.177
        return (0.1238 * PWM) + 10.545

# takes
#   PWM_l_prev: float,
#   PWM_r_prev: float,
#   lane_error_pix: int,
#   time since last call, dt: float,
#   stop_marker_seen: bool
# returns
#   (PWM_l, PWM_r): (float, float)
def get_PWMs_from_visual(lane_error_pix, dt, PWM_l_prev, PWM_r_prev, turn_direction):
    # translate pixel error from center of bot to center of lane to theta
    # tan(theta) = o/a = lane error in centimeters / dist from ROI center to bot center
    # theta = arctan(lane error in centimeters / dist from ROI center to bot center)
    theta = lane_error_pix / PIX_PER_CM

    # store past thetas and calculate moving average theta_dot
    previous_thetas.append(theta)
    previous_theta_dts.append(dt)
    if len(previous_thetas) > THETA_VEL_WINDOW:
        previous_thetas.popleft()
        previous_theta_dts.popleft()
    avg_theta = sum(previous_thetas) / len(previous_thetas)
    # better calculation: compute theta vel for each dt and then average
    theta_velocity = avg_theta / sum(previous_theta_dts)

    # use equation to determine delta_PWM (delta_PWM ~ theta_acceleration)
    delta_vel = - K * theta - B * theta_velocity

    # return PWMs
    vel_l = convert_PWM_to_vel(PWM_l_prev) + delta_vel
    vel_r = convert_PWM_to_vel(PWM_r_prev) - delta_vel
    PWM_l = convert_vel_to_PWM(vel_l)
    PWM_r = convert_vel_to_PWM(vel_r)

    if DEBUG_INFO_ON:
        print("Visual Controller")
        print("{:>22} : {}".format("lane_error_pix", lane_error_pix))
        print("{:>22} : {}".format("dt", dt))
        print("{:>22} : {}".format("PWM_l_prev", PWM_l_prev))
        print("{:>22} : {}".format("PWM_r_prev", PWM_r_prev))
        print("{:>22} : {}".format("theta", theta))
        print("{:>22} : {}".format("theta_velocity", theta_velocity))
        print("{:>22} : {}".format("delta_vel", delta_vel))
        print("{:>22} : {}".format("PWM_l", PWM_l))
        print("{:>22} : {}".format("PWM_r", PWM_r))
        print("="*30)


    return PWM_l, PWM_r

def clear_visual_globals():
    previous_thetas.clear()
    previous_theta_dts.clear()

prev_t = 0
prev_encoder_sum = 0

def visual_compute_motor_values(t, delta_t, left_encoder, right_encoder, delta_left_encoder, delta_right_encoder, left_motor_prev, right_motor_prev, turn_direction, cam):
    global stopping, adjusted_speed, prev_t, prev_encoder_sum

    PWM_l, PWM_r = 0, 0
    lane_error_pix, stop_marker_seen, saw_green = cam.get_error(turn_direction)

    # print("left_encoder", left_encoder)
    # print("right_encoder", right_encoder)
    # print("delta_left_encoder", delta_left_encoder)
    # print("delta_right_encoder", delta_right_encoder)

    # store past thetas and calculate moving average theta_dot
    cur_encoder_avg = (delta_left_encoder + delta_right_encoder)/2
    previous_encoders.append(cur_encoder_avg)
    previous_encoder_dts.append(delta_t)
    if len(previous_encoders) > ENCODER_VEL_WINDOW:
        previous_encoders.popleft()
        previous_encoder_dts.popleft()
    avg_encoder = sum(previous_encoders)
    # print("avg_encoder", avg_encoder)
    # print("sum(previous_encoder_dts)", sum(previous_encoder_dts))
    # print("CM_PER_TICK", CM_PER_TICK)
    true_speed = CM_PER_TICK * avg_encoder / sum(previous_encoder_dts)
    print("true_speed", true_speed)

    # speed calc
    adjustment_factor = 0.005
    # adjustment_factor = 0.1  #sine wave mode
    error = STRAIGHT_SPEED_LIMIT - true_speed
    adj_to_speed = adjustment_factor * error
    adjusted_speed += adj_to_speed

    # print("adjustment_factor", adjustment_factor)
    # print("adj_to_speed", adj_to_speed)
    # print("adjusted_speed", adjusted_speed)


    # TODO: Alex B., check this
    # PWM_l_prev, PWM_r_prev = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT), convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)
    PWM_l_prev, PWM_r_prev = convert_vel_to_PWM(adjusted_speed), convert_vel_to_PWM(adjusted_speed)

    if stop_marker_seen or stopping:
        if DEBUG_INFO_ON:
            print("Stopping On Red")
            print("{:>22} : {}".format("lane_error_pix", lane_error_pix))
            print("{:>22} : {}".format("dt", delta_t))
            print("{:>22} : {}".format("stop_marker_seen", stop_marker_seen))
            print("{:>22} : {}".format("PWM_l_prev", PWM_l_prev))
            print("{:>22} : {}".format("PWM_r_prev", PWM_r_prev))
            print("{:>22} : {}".format("PWM_l", PWM_l))
            print("{:>22} : {}".format("PWM_r", PWM_r))
            print("="*30)

        # TODO: may need to stop more suddenly for the green LEDs
        # PWM_l = convert_vel_to_PWM(convert_PWM_to_vel(PWM_l_prev) / 2)
        # PWM_r = convert_vel_to_PWM(convert_PWM_to_vel(PWM_r_prev) / 2)
        stopping = True

        PWM_l = 0
        PWM_r = 0

        if saw_green:
            ## If we want to pass right through the easiest way is to reuse the previous values
            return left_motor_prev, right_motor_prev, True
        else:
            return PWM_l, PWM_r, False

    PWM_l, PWM_r = get_PWMs_from_visual(lane_error_pix, delta_t, PWM_l_prev, PWM_r_prev, turn_direction)

    # make sure that we send something valid to the motors
    PWM_l = np.clip(PWM_l, -400, 400)
    PWM_r = np.clip(PWM_r, -400, 400)

    return PWM_l, PWM_r, False


def test():
    return get_PWMs_from_visual(20, 0.1, 150, 150, "left")
