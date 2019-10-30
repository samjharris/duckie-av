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
import time
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

timeslice = .25
x_act = [0,0,0]
PWM_l, PWM_r, curr_time = 0, 0, 0
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
        print("arduino->pi: encoder: {} {}".format(left_ticks, right_ticks))

        # translate encoder values to distances and generate new PWMs
        dist_l, dist_r = get_distances(l_ticks - curr_l_ticks,
                                       r_ticks - curr_r_ticks)
        x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
        x_act = x_act_new
        curr_l_ticks = l_ticks
        curr_r_ticks = r_ticks
        PWM_l, PWM_r = get_PWMs(x_ref, curr_time, x_act, PWM_l, PWM_r)

        # send the new motor signals
        print("pi->arduino: motor: {} {}".format(PWM_l, PWM_r))
        message = "{} {}\n".format(left_motor, right_motor)
        to_write = bytearray(message.encode("ascii"))
        ser.write(to_write)
