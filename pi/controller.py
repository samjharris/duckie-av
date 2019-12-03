# CICS 503 Fall 2019 DuckieTown Group 4
#
# controller.py:
# handles the robot-driving logic flow and serial 
# communications with our external hardware, i.e. 
# Arduino Uno, camera, ultrasonic dist. sensor

from config import *
from serial import Serial
from serial.tools.list_ports import comports as get_serial_ports
import struct
from time import time
from visual_control import compute_motor_values, convert_vel_to_PWM, cam
from path_planner import plan_path

debug_mode = False
turn_direction = TURN_DIRECTION


# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]

if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()

#create the serial connection object
ser = Serial(port=ports[0], baudrate=115200)
ser.flushInput()

#ser.close()

last_write = time()
start_time = 0
received_first_message = False

# Previous motor PWM values
l_motor_prev = 0 
r_motor_prev = 0

# Previous encoder tick values
l_encod_prev = 0 
r_encod_prev = 0

#IDEA: to resume after error mid-run, have the option of running the controller.py
#script with a file. When you run with CLI, you input a path and on Ctrl+C the path and
#current position is writen to an output file. Then we can reposition the bot and run:
# ">python controller.py progress.txt" to pick back where we left off.

# Get the user input path
path_input = input("Enter a list of nodes to traverse:")
instructions, full_path = plan_path(path_input)

# This variable will hold the last node we successfully reached
current_node = full_path[0]

# TODO: MORE SETUP

# Okay, setup is done. Here are some helper functions which handle the heavy lifting:
def waitForGreen():
    #Don't care how you do it, just wait for a green light
    return

def traverseIntersection(instruction, ser):
    #Somehow, get across that intersection
    return

def traverseStraightaway(instruction, ser):
    #TODO
    return

def write_motors(left_motor, right_motor, ser):
        global last_write, l_motor_prev, r_motor_prev
        last_write = time()
        to_write = struct.pack('hhc', int(left_motor), int(right_motor), b'A')
        ser.write(to_write)
        l_motor_prev, r_motor_prev = left_motor, right_motor
        return

# Now, time for the control-loop:

# While we still have work to do
while instructions:
    # Pop the next instruction off the stack
    instruction = instructions.pop(0)

    # First, wait for a green light:
    waitForGreen()

    # Then, execute the current instruction:
    ## TURN (providing the instruction, serial-object):
    traverseIntersection(instruction, ser)
    ## Then DRIVE...
    ### (We need to know the side of the road to hug)
    if(instruction == "L"):
        curve = "wide"  # We are going to be taking a wide turn, so hug the white
    elif(instruction == "R"):
        curve = "sharp" # We are going to be taking a sharp turn, so hug the yellow
    else:#instruction == "S"
        curve = "wide"  # We are going straight, so might as well stay away from other cars
    ## ...(providing the curve-type, serial-object):
    traverseStraightaway(curve, ser) #*this funciton should only return when we arrive at a stop light

#Sam todo:
#-Remove read junk & encoder junk from visual control & control loop below
#-Implement traverseStraightaway

#Anyone else todo:
#-Implement traverseIntersection
#-Implement waitForGreen()



#gutted old-code: (still picking this apart)
'''
    bytes_buffer = b""
    buffer_i = 0
    with tqdm(desc="serial") as pbar:
        while True:
            try:
                if ser.in_waiting > 0:
                    new_byte = ser.read()
                    #print(bytes_buffer, " -> ", len(bytes_buffer))
                    # wait until we have recieved consecutive data
                    # in the format: [DEADxxxxxxxxCAFE]
                    if len(bytes_buffer) == 0 and new_byte != b'\xde':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 1 and new_byte != b'\xad':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 6 and new_byte != b'\xca':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 7 and new_byte != b'\xfe':
                        bytes_buffer = b""
                        continue

                    bytes_buffer += new_byte

                    if len(bytes_buffer) == 8:
                        # extract the encoder values
                        left_encoder, right_encoder = struct.unpack('<hh', bytes_buffer[2:6])
                        if debug_mode:
                            print("arduino->pi encoder values (l,r): ", "(", left_encoder, ") (" , right_encoder,")")
                            # print("arduino->pi {:08b}".format(int(bytes_buffer.hex(),16)))
                        bytes_buffer = b""

                        if not received_first_message:
                            start_time = time()
                            left_encoder_previous_value, right_encoder_previous_value = left_encoder, right_encoder
                            left_motor_prev, right_motor_prev = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT), convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)
                            prev_t = 0
                            received_first_message = True

                        t = time() - start_time
                        delta_t = t - prev_t
                        prev_t = t

                        # compute the encoder deltas
                        delta_left_encoder = left_encoder - left_encoder_previous_value
                        delta_right_encoder = right_encoder - right_encoder_previous_value

                        # ask the controller what to do
                        # print("{: >20}{}".format("left_motor_prev",left_motor_prev))
                        # print("{: >20}{}".format("right_motor_prev",right_motor_prev))
                        left_motor, right_motor = compute_motor_values(t, delta_t, left_encoder, right_encoder, delta_left_encoder, delta_right_encoder, left_motor_prev, right_motor_prev, turn_direction)
                        left_encoder_previous_value, right_encoder_previous_value = left_encoder, right_encoder


                        # do what the controller said to do
                        write_motors(left_motor, right_motor)

                        # pbar.update()  # only to measure communication delay

                else:
                    curr_time = time()
                    if curr_time - last_write > 0.01:
                        # write_motors(0, 0)
                        write_motors(left_motor_prev, right_motor_prev)
                        sleep(0.01)

            except KeyboardInterrupt:
                print('Interrupted with ctrl+c')
                try:
                    cam.should_stop = True
                    write_motors(0, 0)
                    break
                except SystemExit:
                    break
'''