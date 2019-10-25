# import serial
# import serial.tools.list_ports as list_ports
# import struct
# import time
# import sys
# import random

# returns the distance (centimeter) traveled
def tick_to_centimeter(ticks):
        # based on the circumfrance of the wheel and the number of steps on encoder
        distance_per_tick = 22.0/26.0
        return ticks*distance_per_tick


# returns the distances traveled by each wheel
def get_distances(left_ticks, right_ticks):
        left_distance = tick_to_centimeter(left_ticks)
        right_distance = tick_to_centimeter(right_ticks)
        return left_distance, right_distance


## handled in closed loop controller
# sys.path.append('../pi')
# import ticks_to_distance as ticks_to_distance

# connect to the open serial port
#ports = list(list_ports.comports())
#ports = [p[0] for p in ports]
#if len(ports) == 0:
#    print("error, couldn't find any open ports")
#    exit()
#print("found open ports: {}".format(ports))

### set the baud rate - this must match the uno's
#baud_rate = 115200
##baud_rate = 9600

###initialize our serial connection
#s_con = serial.Serial(ports[0], baud_rate)
#s_con.flushInput()

## to establish handshake with arduino to sent PWM value for motors.
#comp_list = ["Motor Values? Pi\r\n"]

#start_time = int(round(time.time() * 1000))

###begin control loop
#while True:
#	if s_con.inWaiting() > 0:

#		inputValue = s_con.readline()

#		print(inputValue) #checking
#		# check message in the Serial
#		# TODO: set some delay so the PWM won't be continuously pass to Arduino
#		# also currently, when PWM is pass in, it always ends up in the
#		# fault

#		if inputValue in comp_list:
#			# try:
#			current_time = int(round(time.time() * 1000))
#			print("time difference: %d milliseconds" %(current_time-start_time))
#			if current_time - start_time > 500:
#				# TODO: change to get the new PWM values
#				# also hasn't check if the values passed in actually corresponds
#				# to the correct wheel.
#				right_value,left_value = random.randint(0, 200), random.randint(0, 200)
#				print("right %d, left %d" %(right_value,left_value))
#				# pass the values to Arduino
#				# if want to pass more Int values add to '>BB', each B means
#				# one byte value pass in the serial.  On Arduino's side,
#				# Serial.read() will be turn it back into int.
#				s_con.write(struct.pack('>BB', right_value, left_value))
#				start_time = current_time
#			else:

#				print("not enough time")
#				continue
#			# except:
#			# 	print("error passing motor values")
#			# 	s_con.write('0')

#		# check if Arudiono is trying to pass in the tick values
#		if len(inputValue.split()) != 2:
#			continue

#		love = inputValue.strip()
#		left_ticks, right_ticks = [int(x) for x in love.split()]
#		# print(left_ticks, right_ticks)

#		left_distance, right_distance = get_distances(left_ticks, right_ticks)
#		print("distances: ", left_distance, right_distance)

#		# not sure if this is the right way to do delay.
#		time.sleep(0.2)
