# CICS 503 Fall 2019 DuckieTown Group 4
# Closed loop controller
# Pseudocode:
# initialize x_act, PWM_L, PWM_R, time to zeros
# get path function
# in a loop
#     give all these to closed loop control function and get back new PWMs
#     give PWMs to arduino
#     wait for timeslice time
#     get left and right distance deltas from arduino
#     update x_act

import numpy as np
import time
import positions
from pi_serial import SerialCon
from odometry_guided_feedback import get_PWMs
from ticks_to_distance import get_distances
from struct import *

quad_marker = 1145128260
# quad_marker = int("deadbeef", 16)
quad_marker_bytes = pack('I', quad_marker)
sonar_marker = int("deaffeed", 16)
PWM_begin_marker = int("deadbeef", 16)
timeslice = .25
x_act = [0,0,0]
PWM_L, PWM_R, curr_time = 0, 0, 0
x_ref = positions.get_x_ref_func_one_meter()
curr_l_ticks = 0
curr_r_ticks = 0

##Initialize serial communication
sc = SerialCon()
ports = sc.getOpenPorts()
if not ports:
        print("No open serial ports, exiting")
        exit()
#Select & set appropriate port
port = ports[0]
sc.setPort(port)
#Set appropriate baud rate
sc.setBaud(115200)
#Initialize the connection
sc.initConnection()

counter = 0
while True:
    print("counter: {}".format(counter))
    counter += 1
    PWM_L, PWM_R = get_PWMs(x_ref, curr_time, x_act, PWM_L, PWM_R)
    ##Send to PWMs to Arduino
    msg_out = pack('Iii', PWM_begin_marker, 0, 0)
    # msg_out = pack('Iii', PWM_begin_marker, PWM_L, PWM_R)
    sc.write(msg_out)
    time.sleep(timeslice)
    curr_time += timeslice
    # Wait for input from Arduino: wheel distances as dist_l and dist_r
    msg_in = []
    while True:
        # read in a byte at a time: verify DEADBEEF, then read the rest of the line
        found_deadbeef = False
        for i in range(4):
            char_in = sc.readN(1)
            if char_in != quad_marker_bytes[i]:
                break
            if i == 3:
                found_deadbeef = True
        if found_deadbeef:
            msg_in = sc.readAll()
            print("msg_in: {}".format(msg_in))
            print("len(msg_in): {}".format(len(msg_in)))
    # translate msg_in into left and right ticks and ping output
    # format 16 bytes, start with deadbeef for quadrature and deaffeed end with newline
    l_ticks, r_ticks, junk_1, junk_2 = unpack('iiic', msg_in)
    dist_l, dist_r = get_distances(l_ticks - curr_l_ticks, r_ticks - curr_r_ticks)
    x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
    x_act = x_act_new
    curr_l_ticks = l_ticks
    curr_r_ticks = r_ticks
    print(dist_l)
    print(dist_r)
    print(PWM_L)
    print(PWM_R)
