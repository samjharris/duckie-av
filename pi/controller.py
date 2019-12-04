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
from time import sleep, time
from tqdm import tqdm
from numpy import int32, float64
# from visual_control import compute_motor_values, convert_vel_to_PWM, cam
from visual_control import convert_vel_to_PWM, cam
from open_loop import compute_motor_values

debug_mode = False
turn_direction = TURN_DIRECTION

# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]

if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
with Serial(port=ports[0], baudrate=115200) as ser:
    ser.flushInput()

    last_write = time()
    left_motor_prev, right_motor_prev = 0, 0
    def write_motors(left_motor, right_motor):
        global last_write, left_motor_prev, right_motor_prev

        # print(left_motor, right_motor)

        # assert type(left_motor) in [int, float, int32, float64], "motor input should be of type int, not {}".format(type(left_motor))
        # assert type(right_motor) in [int, float, int32, float64], "motor input should be of type int, not {}".format(type(right_motor))

        last_write = time()
        to_write = struct.pack('hhc', int(left_motor), int(right_motor), b'A')
        if debug_mode:
            print("pi->arduino", left_motor, right_motor)
            # print("pi->arduino {:08b}".format(int(to_write.hex(),16))[:-8])
        ser.write(to_write)
        left_motor_prev, right_motor_prev = left_motor, right_motor

    start_time = 0
    received_first_message = False
    left_encoder_previous_value, right_encoder_previous_value = 0, 0

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
