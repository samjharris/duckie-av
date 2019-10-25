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
from pi.ticks_to_distance import get_distances
from struct import *

quad_marker = int("deadbeef", 16)
sonar_marker = int("deaffeed", 16)
PWM_begin_marker = int("deadbeef", 16)
PWM_end_marker = int("beefdead", 16)
timeslice = .25
x_act = [0,0,0]
PWM_L, PWM_R, curr_time = 0, 0, 0
x_ref = positions.get_x_ref_func_one_meter()

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

while True:
    PWM_L, PWM_R = get_PWMs(x_ref, curr_time, x_act, PWM_L, PWM_R)
    ##Send to PWMs to Arduino
    msg_out = pack('Iii', PWM_begin_marker, 0, 0)
    # msg_out = pack('Iii', PWM_begin_marker, PWM_L, PWM_R)
    sc.write(msg_out)
    time.sleep(timeslice)
    curr_time += timeslice
    ##Wait for input from Arduino: wheel distances as dist_l and dist_r
    msg_in = sc.read_Line()
    # translate msg_in into left and right ticks and ping output
    # format 16 bytes, start with deadbeef for quadrature and deaffeed end with newline
    msg_marker, l_ticks, r_ticks = unpack('Iii', msg_in)
    if msg_marker != quad_marker:
        raise Exception('Message marker is not deadbeef')
    dist_l, dist_r = get_distances(l_ticks, r_ticks)
    x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
    x_act = x_act_new
    print(dist_l)
    print(dist_r)
    print(PWM_L)
    print(PWM_R)
