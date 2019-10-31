# CICS 503 Fall 2019 DuckieTown Group 4
# Positions Module
# Contains routing and position functions

# takes some route information and returns a route function
# def get_x_ref_func():

import numpy as np

def get_x_ref_func_one_meter():
    timeslice = 0.5 # fraction of a second; resolution of our function
    endgoal = 100 # goal is one meter measured in centimeters
    speed_goal = 5 # cm/s
    total_time = endgoal / speed_goal
    amount_of_slices = total_time / timeslice
    position_by_time_list = []
    for i in range(int(amount_of_slices) + 1):
        position_by_time_list.append(np.array([(speed_goal * (i / 4)), 0, 0]))
    def x_ref_func_one_meter(t):
        index = int(t / timeslice)
        length = len(position_by_time_list)
        if index >= length:
            return position_by_time_list[length - 1]
        else:
            return position_by_time_list[index]
    return x_ref_func_one_meter

def get_x_ref_func_circle():
    timeslice = 0.5
    speed_goal = 5 # cm/s
    radius = 10
    circumference = 2 * np.pi * radius
    time_to_circle = circumference / speed_goal
    timeslices_per_circle = time_to_circle / timeslice
    delta_theta_per_timeslice = 360 / timeslices_per_circle
    num_circles = 5
    total_time = time_to_circle * num_circles
    amount_of_slices = total_time / timeslice
    position_by_time_list = []
    x = 0
    y = 0
    theta = 0
    for i in range(int(amount_of_slices) + 1):
        x = radius * np.sin(np.deg2rad(theta))
        y = radius * (1 - np.cos(np.deg2rad(theta)))
        position_by_time_list.append(np.array([x,y,theta]))
        theta = (theta + delta_theta_per_timeslice) % 360
    def x_ref_func_circle(t):
        index = int(t / timeslice)
        length = len(position_by_time_list)
        if index >= length:
            return position_by_time_list[length - 1]
        else:
            return position_by_time_list[index]
    return x_ref_func_circle


def get_x_act_new(x_act_prev, dist_l, dist_r):
    dist_diff = dist_r - dist_l

    # print("dist_diff (should be 0)", dist_diff)

    wheelbase = 16.5

    # delta_theta = np.rad2deg(np.arctan2[dist_diff],[wheelbase])
    delta_theta = np.rad2deg(dist_diff/wheelbase) % 360
    # print("delta_theta (should be ~0)", delta_theta)
    new_theta = x_act_prev[2] + delta_theta
    # print("new_theta (should be ~0)", new_theta)
    avg_theta = x_act_prev[2] + delta_theta / 2
    # print("avg_theta (should be ~0)", avg_theta)

    # TODO update with better approximation
    delta_x_length = (dist_l + dist_r) / 2
    # print("delta_x_length", delta_x_length)

    delta_x_x_component = delta_x_length * np.cos(np.deg2rad(avg_theta))
    delta_x_y_component = delta_x_length * np.sin(np.deg2rad(avg_theta))
    # print("delta_x_x_component", delta_x_x_component)
    # print("delta_x_y_component", delta_x_y_component)

    new_x_act_x_component = x_act_prev[0] + delta_x_x_component
    new_x_act_y_component = x_act_prev[1] + delta_x_y_component
    # print("new_x_act_x_component", new_x_act_x_component)
    # print("new_x_act_y_component", new_x_act_y_component)

    new_theta = new_theta % 360
    # print("new_theta", new_theta)

    return (new_x_act_x_component, new_x_act_y_component, new_theta)

def test():
    x = get_x_ref_func_one_meter()
    y = get_x_ref_func_circle()
    for i in range(10):
        print(x(i))
        print(y(i))
