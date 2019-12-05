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
from time import time, sleep
from visual_control import visual_compute_motor_values, convert_vel_to_PWM
from open_control import open_compute_motor_values
from path_planner import plan_path

class Controller():
    def __init__(self, instructions, full_path):
        #Control type: 0 for visual, 1 for open, 2 for stopped
        self.control_type = CONTROL_VISUAL #start in visual (we will see red), then wait for geen
        
        self.instructions = instructions
        self.full_path = full_path

        # turn_type: 'L' for left, 'R' for right, 'S' for straight
        self.instruction = self.instructions.pop(0)
        # hug: 0 for white, 1 for yellow
        self.hug = HUG_WHITE
        # prev_hug: 0 for white, 1 for yellow
        self.prev_hug = HUG_WHITE
        #self.cur_node = full_path[0]
        #self.nxt_node = full_path[1]

    def compute_motor_values(self, t, delta_t, l_encod, r_encod, delta_l_encod, delta_r_encod, l_motor_prev, r_motor_prev):
        l_motor = 0
        r_motor = 0 
        
        saw_red = False
        saw_green = False
        done = False

        #compute motor values
        if(self.control_type == CONTROL_VISUAL): #visual control
            l_motor,r_motor,saw_red,saw_green = visual_compute_motor_values(t, delta_t, l_encod, r_encod, delta_l_encod, delta_r_encod, l_motor_prev, r_motor_prev, self.hug)
        elif(self.control_type == CONTROL_OPEN): #open-loop control
            l_motor,r_motor,done = open_compute_motor_values(self.prev_hug, self.instruction, delta_l_encod, delta_r_encod)
        else: #self.control_type == CONTROL_STOP we are "stopped"
            l_motor,r_motor = 0, 0
            return l_motor, r_motor
        
        #update state
        if saw_red:
            if not instructions: #no more instructions, we are done
                self.control_type = CONTROL_STOP
                return l_motor, r_motor
            if saw_green:
                self.control_type = CONTROL_OPEN
                self.instruction = instructions.pop(0)
                self.prev_hug = self.hug
                if self.instruction == TURN_R:
                    self.hug = HUG_YELLOW #Right, hug yellow
                elif self.instruction == TURN_L:
                    self.hug = HUG_WHITE #Left, hug white
                else:
                    self.hug = self.prev_hug #Straight, hug the same as before
        elif done:
            self.control_type = CONTROL_VISUAL

        return l_motor, r_motor

if __name__ == "__main__":
    # connect to the open serial port
    ports = [p[0] for p in get_serial_ports()]

    if len(ports) == 0:
        print("Error, couldn't find any open ports")
        exit()

    #create the serial connection object
    with Serial(port=ports[0], baudrate=115200) as ser:
        ser.flushInput()


        last_write = time()
        received_first_message = False

        # Previous motor PWM values (initialized to an estimate, to avoid buggy startup behavior)
        l_motor = 0
        l_motor_prev = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)
        r_motor = 0
        r_motor_prev = convert_vel_to_PWM(STRAIGHT_SPEED_LIMIT)

        # Encoder tick values
        l_encod = 0
        l_encod_prev = 0 
        r_encod = 0
        r_encod_prev = 0

        # Get the user input path
        path_input = input("Enter a list of nodes to traverse:")
        instructions, full_path = plan_path(path_input)
        # Instantiate our controller
        cont = Controller(instructions, full_path)

        # These variables will hold the incoming serial data
        bytes_buffer = b""
        buffer_i = 0

        # Now, time for the control-loop:
        while True:
            try:
                if ser.in_waiting > 0:
                    new_byte = ser.read()
                    # wait until we have recieved consecutive data
                    # in the format: [DEADxxxxxxxxCAFE]
                    if len(bytes_buffer) == 0 and new_byte != b'\xde':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 1 and new_byte != b'\xad':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 8 and new_byte != b'\xca':
                        bytes_buffer = b""
                        continue
                    if len(bytes_buffer) == 9 and new_byte != b'\xfe':
                        bytes_buffer = b""
                        continue
                    #accept this byte as valid
                    bytes_buffer += new_byte

                    if len(bytes_buffer) == 10:
                        # extract the encoder values, and ping_distance (0 means nothing detected)

                        l_encod, r_encod, ping_distance = struct.unpack('<hhh', bytes_buffer[2:8])
                        bytes_buffer = b""

                        if not received_first_message:
                            start_time = time()
                            l_encod_prev, r_encod_prev = l_encod, r_encod
                            t_prev = 0
                            received_first_message = True

                        t = time() - start_time
                        delta_t = t - t_prev
                        t_prev = t

                        # compute the encoder deltas
                        delta_l_encod = l_encod - l_encod_prev
                        delta_r_encod = r_encod - r_encod_prev

                        # ask the controller what to do
                        l_motor, r_motor = cont.compute_motor_values(t, delta_t, l_encod, r_encod, delta_l_encod, delta_r_encod, l_motor_prev, r_motor_prev)
                        #l_motor,r_motor,done = open_compute_motor_values(HUG_WHITE, "left", delta_l_encod, delta_r_encod)
                        
                        # do what the controller said to do
                        to_write = struct.pack('hhc', int(l_motor), int(r_motor), b'A')
                        ser.write(to_write)
                        last_write = time()
                        
                        # now, the current values are the previous
                        l_motor_prev = l_motor
                        l_motor_prev = r_motor
                        l_encod_prev = l_encod
                        r_encod_prev = r_encod


                else:
                    if time() - last_write > 0.01:
                        to_write = struct.pack('hhc', int(l_motor_prev), int(r_motor_prev), b'A')
                        ser.write(to_write)
                        last_write = time()
                        sleep(0.01)
                pass
            except KeyboardInterrupt:
                print('Interrupted with ctrl+c')
                try:
                    # Controller.cam.should_stop = True
                    to_write = struct.pack('hhc', 0, 0, b'A')
                    ser.write(to_write)
                    # ser.close()
                    break
                except SystemExit:
                    break
    #Clean-up
    # ser.close()