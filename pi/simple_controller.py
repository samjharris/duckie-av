from serial import Serial
from serial.tools.list_ports import comports as get_serial_ports


# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
ser = Serial(port=ports[0], baudrate=9600)
# ser = Serial(port=ports[0], baudrate=115200)
ser.flushInput()


while True:
	if ser.inWaiting():
		# receive the encoder values
		inputValue = ser.readline().decode("utf-8").strip()
		print(inputValue)
		if len(inputValue.split()) != 3:
			print("mode 1: input was '{}'".format(inputValue))
			continue
		if inputValue.split()[0] != "encoder":
			print("mode 2: input was '{}'".format(inputValue))
			continue

		_, left_ticks, right_ticks = inputValue.split()
		print("arduino->pi: encoder: {} {}".format(left_ticks, right_ticks))

		# send the new motor signals
		# left_motor, right_motor = 300, 300
		left_motor, right_motor = 0, 0
		print("pi->arduino: motor: {} {}".format(left_motor, right_motor))
		message = "{} {}\n".format(left_motor, right_motor)
		to_write = bytearray(message.encode("ascii"))
		ser.write(to_write)
