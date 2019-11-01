
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

from closed_loop_controller_header import *

# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
ser = Serial(port=ports[0], baudrate=BAUDRATE)
ser.flushInput()

start_time = time() + TIME_SLICE
curr_time = 0
last_time = 0
delta_time = 0

x_act = np.array([0,0,0])
x_act_prev = np.array([0,0,0])

PWM_l, PWM_r = 0, 0
x_ref_func = positions.get_x_ref_func_one_meter()
curr_l_ticks = 0
curr_r_ticks = 0

received_start_signal = False








import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()

world_line, = plt.plot([0,0,100], [100,0,0], color='black', animated=True)

bot_line, = plt.plot([0], [0], color='red', animated=True)
x_ref_line, = plt.plot([0], [0], color='green', animated=True)




def init():
    ax.set_xlim(-100, 200)
    ax.set_ylim(-150, 150)
    return [world_line, bot_line, x_ref_line]


def update(frame):
    global start_time
    global curr_time
    global last_time
    global delta_time

    global x_act
    global x_act_prev

    global PWM_l, PWM_r
    global x_ref_func
    global curr_l_ticks
    global curr_r_ticks

    global received_start_signal

    try:

        if ser.inWaiting():
            # receive the encoder values
            inputValue = ser.readline().decode("utf-8").strip()
            args = inputValue.split()
            if inputValue == "":
                return [world_line, bot_line, x_ref_line]
            if not received_start_signal:
                if inputValue == "arduino start":
                    received_start_signal = True
                    start_time = time() + TIME_SLICE
                    return [world_line, bot_line, x_ref_line]
                else:
                    return [world_line, bot_line, x_ref_line]

            if args[0] != "encoder":
                print("error 2: input was '{}'".format(inputValue))
                return [world_line, bot_line, x_ref_line]
            if len(args) != 3:
                print("error 1: input was '{}'".format(inputValue))
                return [world_line, bot_line, x_ref_line]

            _, delta_l_ticks, delta_r_ticks = args
            # print("arduino->pi: encoder: {} {}".format(delta_l_ticks, delta_r_ticks))
            delta_l_ticks, delta_r_ticks = int(delta_l_ticks), int(delta_r_ticks)

            # translate encoder values to distances and generate new PWMs
            dist_l, dist_r = get_distances(delta_l_ticks, delta_r_ticks)
            x_act_new = positions.get_x_act_new(x_act, dist_l, dist_r)
            x_act = x_act_new
            curr_l_ticks = delta_l_ticks
            curr_r_ticks = delta_r_ticks
            curr_time = time() - start_time
            delta_time = curr_time - last_time
            PWM_l, PWM_r = get_PWMs(x_ref_func, curr_time, delta_time, x_act, x_act_prev, PWM_l, PWM_r)
            x_act_prev = x_act
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
            ser.close()
            exit()
            # exit()
        except SystemExit:
            ser.close()
            exit()



    angles = x_act[-1] + np.array( [ - np.pi/6, np.pi/6, np.pi - np.pi/6, np.pi + np.pi/6, - np.pi/6 ] )
    bot_line_x = 10 * np.cos(angles) + x_act[0]
    bot_line_y = 10 * np.sin(angles) + x_act[1]

    bot_line.set_data(bot_line_x, bot_line_y)
    x_ref_line.set_data(25, 0)

    return [world_line, bot_line, x_ref_line]



print("loading visualizer")
fps = 20
ftime = 1000/fps # delay between frames in milliseconds

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100000),
                    init_func=init, interval=ftime, blit=True)

# plt.axis('equal')
plt.show()





PWM_l, PWM_r = 0, 0
message = "{} {}\n".format(PWM_l, PWM_r)
to_write = bytearray(message.encode("ascii"))
ser.write(to_write)
ser.close()
