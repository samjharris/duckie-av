from serial import Serial
from serial.tools.list_ports import comports as get_serial_ports
import struct
from time import sleep, time
from tqdm import tqdm


# connect to the open serial port
ports = [p[0] for p in get_serial_ports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
# ser = Serial(port=ports[0], baudrate=9600)
ser = Serial(port=ports[0], baudrate=115200)
ser.flushInput()

last_write = time()

# bytes_buffer = bytearray(4)
bytes_buffer = b""
buffer_i = 0
with tqdm(total=1) as pbar:
	while True:
		if ser.in_waiting > 0:
			new_byte = ser.read()
			# print(new_byte)

			# grooble = ser.read_until('A')
			# print(grooble)


			if len(bytes_buffer) == 4:
				# new_byte == b'A'
				# print("arduino->pi", bytes_buffer)
				binary_string = "arduino->pi {:08b}".format(int(bytes_buffer.hex(),16))
				print(binary_string)

				left_encoder, right_encoder = struct.unpack('<hh', bytes_buffer)
				print("arduino->pi", left_encoder, right_encoder)

				bytes_buffer = b""
				pbar.update()

			else:
				bytes_buffer += new_byte
				# bytes_buffer[buffer_i] = int(new_byte)
				# buffer_i += 1


		else:
			# print("nope, no serial data yet")
			# if buffer_i == 0 and ser.out_waiting == 0:
			curr_time = time()
			if curr_time - last_write > 0.01:

				last_write = time()
				left_motor, right_motor = -257, 21000
				print("pi->arduino", left_motor, right_motor)
				to_write = struct.pack('hhc', left_motor, right_motor, b'A')
				# print("pi->arduino", to_write)

				binary_string = "pi->arduino {:08b}".format(int(to_write.hex(),16))[:-8]
				print(binary_string)

				ser.write(to_write)
				sleep(0.01)
				# print(ser.out_waiting)
