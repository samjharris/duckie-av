# using equation theta_2 = -K (theta - theta_ref) - B (theta_dot - theta_1_ref)
# theta_dot = theta_(t+1) - theta_t
from odometry_guided_feedback import convert_PWM_to_vel, convert_vel_to_PWM
from config import *
import numpy as np
from collections import deque

previous_thetas = deque()
previous_dts = deque()

# takes 
#   PWM_l_prev: float,
#   PWM_r_prev: float,
#   lane_error_pix: int,
#   time since last call, dt: float, 
#   stop_marker_seen: bool
# returns 
#   (PWM_l, PWM_r): (float, float)
def get_PWMs_from_visual(lane_error_pix, dt, stop_marker_seen, PWM_l_prev, PWM_r_prev):
    # TODO: start and proceed at speed limit --- Maybe not here

    # TODO: stop on red boolean
    if stop_marker_seen:
        return 0, 0

    # TODO: translate pixel error from center of bot to center of lane to theta
    # tan(theta) = o/a = lane error in centimeters / dist from ROI center to bot center
    # theta = arctan(lane error in centimeters / dist from ROI center to bot center)
    DIST_TO_ROI_CM = 10
    PIX_PER_CM = 100
    lane_error_cm = lane_error_pix / PIX_PER_CM
    theta = np.arctan2(lane_error_cm, DIST_TO_ROI_CM)

    # TODO: store past thetas and calculate moving average theta_dot
    previous_thetas.append(theta)
    previous_dts.append(dt)
    if len(previous_thetas) > 5:
        previous_thetas.popleft()
        previous_dts.popleft()
    avg_theta = sum(previous_thetas) / len(previous_thetas)
    # TODO: better calculation: computer theta vel for each dt and then average
    theta_velocity = avg_theta / sum(previous_dts)

    # TODO: use equation to determine delta_PWM (delta_PWM ~ theta_acceleration)
    delta_PWM = - K * theta - B * theta_velocity

    # handle PWM <==> velocity stuff  
    vel_l_prev = convert_PWM_to_vel(PWM_l_prev)
    vel_r_prev = convert_PWM_to_vel(PWM_r_prev)
    if delta_PWM > 0:
        delta_PWM += MIN_PWM
    if delta_PWM < 0:
        delta_PWM -= MIN_PWM
    delta_vel = convert_PWM_to_vel(delta_PWM)

    # TODO: return PWMs
    PWM_l = convert_vel_to_PWM(vel_l_prev - delta_vel)
    PWM_r = convert_vel_to_PWM(vel_r_prev + delta_vel)

    return PWM_l, PWM_r

def clear_visual_globals():
    previous_thetas.clear()
    previous_dts.clear()

def test():
    return get_PWMs_from_visual(20, 0.1, False, 150, 150)