# CICS 503 Fall 2019 DuckieTown Group 4
# Positions Module
# Contains routing and position functions

# takes some route information and returns a route function
# def get_x_ref_func():

import numpy as np

def get_x_ref_func_one_meter():
    timeslice = 0.25 # fraction of a second; resolution of our function
    endgoal = 100 # goal is one meter measured in centimeters
    speed_goal = 20 # cm/s
    total_time = endgoal / speed_goal
    amount_of_slices = total_time / timeslice
    position_by_time_list = []
    for i in range(int(amount_of_slices) + 1):
        position_by_time_list.append(np.array([(speed_goal * (i / 4)), 0, 0]))
    def x_ref_func_one_meter(t):
        return position_by_time_list[t]
    return x_ref_func_one_meter

def get_x_ref_func_circle():
    timeslice = 0.25
    speed_goal = 20 # cm/s
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
        return position_by_time_list[t]
    return x_ref_func_circle


def get_x_act_new(x_act_prev, dist_l, dist_r):
    dist_diff = dist_r - dist_l

    # TODO measure this
    wheelbase = 1

    # delta_theta = np.rad2deg(np.arctan2[dist_diff],[wheelbase])
    delta_theta = np.rad2deg(dist_diff/wheelbase) % 360
    new_theta = x_act_prev[2] + delta_theta
    avg_theta = x_act_prev[2] + delta_theta / 2

    # TODO update with better approximation
    delta_x_length = (dist_l + dist_r) / 2

    delta_x_x_component = delta_x_length * np.cos(np.deg2rad(avg_theta))
    delta_x_y_component = delta_x_length * np.sin(np.deg2rad(avg_theta))

    new_x_act_x_component = x_act_prev[0] + delta_x_x_component
    new_x_act_y_component = x_act_prev[1] + delta_x_y_component

    return (new_x_act_x_component, new_x_act_y_component, new_theta)

def test():
    x = get_x_ref_func_one_meter()
    y = get_x_ref_func_circle()
    for i in range(10):
        print(x(i))
        print(y(i))
