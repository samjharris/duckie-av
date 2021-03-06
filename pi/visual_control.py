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

cam = Camera()

sleep(1)

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

    if False:
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

def visual_compute_motor_values(t, delta_t, left_encoder, right_encoder, delta_left_encoder, delta_right_encoder, left_motor_prev, right_motor_prev, hug, ping_distance):
    global stopping, adjusted_speed, prev_t, prev_encoder_sum, cam
    global previous_encoders, previous_encoder_dts
    global previous_thetas, previous_theta_dts

    target_speed = STRAIGHT_SPEED_LIMIT
    if(ping_distance > PING_MIN_STRAIGHT and ping_distance < (PING_MIN_STRAIGHT + PING_WINDOW_STRAIGHT)):
        target_speed = target_speed * (ping_distance - PING_MIN_STRAIGHT) / PING_WINDOW_STRAIGHT
    elif (ping_distance < PING_MIN_STRAIGHT and ping_distance > 0):
        target_speed = 0

    PWM_l, PWM_r = 0, 0
    lane_error_pix, saw_red, saw_green = cam.get_error(hug)

    # store past thetas and calculate moving average theta_dot
    cur_encoder_avg = (delta_right_encoder)
    # cur_encoder_avg = (delta_left_encoder + delta_right_encoder)/2
    previous_encoders.append(cur_encoder_avg)
    previous_encoder_dts.append(delta_t)
    
    if len(previous_encoders) > ENCODER_VEL_WINDOW:
        previous_encoders.popleft()
        previous_encoder_dts.popleft()
    avg_encoder = sum(previous_encoders)
    true_speed = CM_PER_TICK * avg_encoder / sum(previous_encoder_dts)
    if False:
        print("true_speed", true_speed)

    # speed calc
    adjustment_factor = 0.01

    # adjustment_factor = 0.1  #sine wave mode
    error = target_speed - true_speed
    adj_to_speed = adjustment_factor * error
    adjusted_speed += adj_to_speed
    adjusted_speed = max(0, adjusted_speed)

    # PWM_l_prev, PWM_r_prev = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT), convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)
    PWM_l_prev, PWM_r_prev = convert_vel_to_PWM(adjusted_speed), convert_vel_to_PWM(adjusted_speed)

    PWM_l, PWM_r = get_PWMs_from_visual(lane_error_pix, delta_t, PWM_l_prev, PWM_r_prev, hug)

    # make sure that we send something valid to the motors
    PWM_l = np.clip(PWM_l, -400, 400)
    PWM_r = np.clip(PWM_r, -400, 400)

    # reset globals when passing control
    if saw_red and saw_green:
        adjusted_speed = 0
        previous_encoders.clear()
        previous_encoder_dts.clear()
        previous_thetas.clear()
        previous_theta_dts.clear()
        stopping = False

    return PWM_l, PWM_r, saw_red, saw_green


def test():
    return get_PWMs_from_visual(20, 0.1, 150, 150, "left")
