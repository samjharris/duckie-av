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
curr_time = 0
last_time = 0
delta_time = 0

x_act = [0,0,0]
PWM_l, PWM_r = 0, 0
x_ref_func = positions.get_x_ref_func_one_meter()
curr_l_ticks = 0
curr_r_ticks = 0

received_start_signal = False

while True:
    try:

        if ser.inWaiting():
            # receive the encoder values
            inputValue = ser.readline().decode("utf-8").strip()
            args = inputValue.split()
            if inputValue == "":
                continue
            if not received_start_signal:
                if inputValue == "arduino start":
                    received_start_signal = True
                else:
                    continue

            if args[0] != "encoder":
                print("error 2: input was '{}'".format(inputValue))
                continue
            if len(args) != 3:
                print("error 1: input was '{}'".format(inputValue))
                continue

            _, delta_l_ticks, delta_r_ticks = args
            # print("arduino->pi: encoder: {} {}".format(delta_l_ticks, delta_r_ticks))
            delta_l_ticks, delta_r_ticks = int(delta_l_ticks), int(delta_r_ticks)

            # translate encoder values to distances and generate new PWMs
            dist_l, dist_r = get_distances(delta_l_ticks, delta_r_ticks)
            x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
            x_act = x_act_new
            curr_l_ticks = delta_l_ticks
            curr_r_ticks = delta_r_ticks
            curr_time = time() + 0.5 - start_time
            delta_time = curr_time - last_time 
            PWM_l, PWM_r = get_PWMs(x_ref_func, curr_time, delta_time, x_act, PWM_l, PWM_r)
            last_time = curr_time
            PWM_l, PWM_r = int(PWM_l), int(PWM_r)

            # send the new motor signals
            assert type(PWM_l) == int, "PWM_l is not int"
            assert type(PWM_r) == int, "PWM_r is not int"
            message = "{} {}\n".format(PWM_l, PWM_r)
            to_write = bytearray(message.encode("ascii"))
            ser.write(to_write)

            print("x_ref_func(curr_time): {}".format(x_ref_func(curr_time)))
            print("x_act: {}".format(x_act))
            print("PWM_l: {}".format(PWM_l))
            print("PWM_r: {}".format(PWM_r))
            print("delta_l_ticks: {}".format(delta_l_ticks))
            print("delta_r_ticks: {}".format(delta_r_ticks))
            print("="*30)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            PWM_l, PWM_r = 0, 0
            message = "{} {}\n".format(PWM_l, PWM_r)
            to_write = bytearray(message.encode("ascii"))
            ser.write(to_write)
            break
            # exit()
        except SystemExit:
            exit()
