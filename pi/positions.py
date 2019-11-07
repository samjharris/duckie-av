# CICS 503 Fall 2019 DuckieTown Group 4
# Positions Module
# Contains routing and position functions

# takes some route information and returns a route function
# def get_x_ref_func():

from config import *
import numpy as np

def get_x_ref_func_one_meter():
    total_time = END_GOAL / STRAIGHT_SPEED_LIMIT
    num_slices = total_time / TIME_SLICE
    position_by_time_list = []
    for i in range(int(num_slices) + 1):
        position_by_time_list.append(np.array([(STRAIGHT_SPEED_LIMIT * (i * TIME_SLICE)), 0, 0]))
    position_by_time_list.append(np.array([END_GOAL, 0, 0]))
    def x_ref_func_one_meter(t):
        index = round(t / TIME_SLICE)
        length = len(position_by_time_list)
        if index >= length:
            return position_by_time_list[length - 1]
        else:
            return position_by_time_list[index]
    return x_ref_func_one_meter


def get_x_ref_func_circle():
    circle_circum = 2 * np.pi * CIRCLE_RADIUS
    time_to_circle = circle_circum / TURN_SPEED_LIMIT
    timeslices_per_circle = time_to_circle / TIME_SLICE
    delta_theta_deg_per_timeslice = 360 / timeslices_per_circle
    num_circles = 5
    total_time = time_to_circle * num_circles
    num_slices = total_time / TIME_SLICE
    position_by_time_list = []
    x = 0
    y = 0
    theta = 0
    for i in range(int(num_slices) + 1):
        x = CIRCLE_RADIUS * np.sin(np.deg2rad(theta))
        y = CIRCLE_RADIUS * (1 - np.cos(np.deg2rad(theta)))
        position_by_time_list.append(np.array([x,y,theta]))
        theta = (theta + delta_theta_deg_per_timeslice) % 360
    def x_ref_func_circle(t):
        index = round(t / TIME_SLICE)
        length = len(position_by_time_list)
        if index >= length:
            return position_by_time_list[length - 1]
        else:
            return position_by_time_list[index]
    def print_debug_info():
        print("{:>22} : {}".format("total_time", total_time))
        print("{:>22} : {}".format("TIME_SLICE", TIME_SLICE))
        print("{:>22} : {}".format("num_slices", num_slices))
    print_debug_info()
    return x_ref_func_circle


def get_x_act_new(x_act_prev, dist_l, dist_r):
    dist_diff = dist_l - dist_r

    # print("dist_diff (should be 0)", dist_diff)

    WHEEL_BASE = 16.5

    # delta_theta_deg = np.rad2deg(np.arctan2[dist_diff],[wheelbase])
    delta_theta_deg = dist_diff/(2 * np.pi * WHEEL_BASE) * 360
    # print("delta_theta_deg (should be ~0)", delta_theta_deg)
    new_theta = (x_act_prev[2] + delta_theta_deg) % 360
    # print("new_theta (should be ~0)", new_theta)

    ys = np.sin(np.deg2rad(x_act_prev[2])) + np.sin(np.deg2rad(delta_theta_deg))
    xs = np.cos(np.deg2rad(x_act_prev[2])) + np.cos(np.deg2rad(delta_theta_deg))
    avg_theta = np.arctan2(ys, xs)

    # avg_theta = x_act_prev[2] + delta_theta_deg / 2
    # print("avg_theta (should be ~0)", avg_theta)

    delta_x_length = (dist_l + dist_r) / 2
    # print("delta_x_length", delta_x_length)

    delta_x_x_component = delta_x_length * np.cos(avg_theta)
    delta_x_y_component = delta_x_length * np.sin(avg_theta)
    # print("delta_x_x_component", delta_x_x_component)
    # print("delta_x_y_component", delta_x_y_component)

    new_x_act_x_component = x_act_prev[0] + delta_x_x_component
    new_x_act_y_component = x_act_prev[1] + delta_x_y_component
    # print("new_x_act_x_component", new_x_act_x_component)
    # print("new_x_act_y_component", new_x_act_y_component)

    return np.array([new_x_act_x_component, new_x_act_y_component, new_theta])

def test():
    x = get_x_ref_func_circle()
    for i in range(6):
        print(x(i/10))
    print('='*30)
    for i in range(1,7):
        print(x(i))
    print('='*30)
    print(x(6.5))
    print(x(6.6))
    print(x(6.7))
    print(x(6.8))
    return x
