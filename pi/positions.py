# CICS 503 Fall 2019 DuckieTown Group 4
# Positions Module
# Contains routing and position functions

# takes some route information and returns a route function
# def get_x_ref_func():

# Takes time in seconds, returns triple [x_coordinate, y_coordinate, theta]
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

def test():
    x = get_x_ref_func_one_meter()
    y = get_x_ref_func_circle()
    for i in range(10):
        print(x(i))
        print(y(i))
