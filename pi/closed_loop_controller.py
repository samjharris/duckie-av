# CICS 503 Fall 2019 DuckieTown Group 4
# Closed loop controller
# Pseudocode:
# initialize x_act, PWM_l, PWM_r, time to zeros
# get path function
# in a loop
#     give all these to closed loop control function and get back new PWMs
#     give PWMs to arduino
#     wait for timeslice time
#     get left and right distance deltas from arduino
#     update x_act

import numpy as np
from time import time
from serial import Serial
from serial.tools.list_ports import comports as get_serial_ports

import positions
from odometry_guided_feedback import get_PWMs
from ticks_to_distance import get_distances

# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
ser = Serial(port=ports[0], baudrate=9600)
# ser = Serial(port=ports[0], baudrate=115200)
ser.flushInput()

start_time = time()
x_act = [0,0,0]
PWM_l, PWM_r = 0, 0
x_ref = positions.get_x_ref_func_one_meter()
curr_l_ticks = 0
curr_r_ticks = 0

while True:
    if ser.inWaiting():
        # receive the encoder values
        inputValue = ser.readline().decode("utf-8").strip()
        if len(inputValue.split()) != 2:
            print("error: input was '{}'".format(inputValue))
            continue

        l_ticks, r_ticks = inputValue.split()
        # print("arduino->pi: encoder: {} {}".format(l_ticks, r_ticks))
        l_ticks, r_ticks = int(l_ticks), int(r_ticks)
        delta_l_ticks = l_ticks - curr_l_ticks
        delta_r_ticks = r_ticks - curr_r_ticks

        # translate encoder values to distances and generate new PWMs
        dist_l, dist_r = get_distances(delta_l_ticks, delta_r_ticks)
        x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
        x_act = x_act_new
        curr_l_ticks = l_ticks
        curr_r_ticks = r_ticks
        curr_time = time() - start_time
        PWM_l, PWM_r = get_PWMs(x_ref, curr_time, x_act, PWM_l, PWM_r)

        # send the new motor signals
        message = "{} {}\n".format(PWM_l, PWM_r)
        to_write = bytearray(message.encode("ascii"))
        ser.write(to_write)

        print("x_ref: {}".format(x_ref))
        print("x_act: {}".format(x_act))
        print("PWM_l: {}".format(PWM_l))
        print("PWM_r: {}".format(PWM_r))
        print("delta_l_ticks: {}".format(delta_l_ticks))
        print("delta_r_ticks: {}".format(delta_r_ticks))
