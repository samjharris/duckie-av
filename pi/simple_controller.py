from serial import Serial
# import serial.tools.list_ports.comports as get_ports
from serial.tools.list_ports import comports as get_ports


# connect to the open serial port
ports = [p[0] for p in get_ports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
print("ports: {}".format(ports))

# 115200
ser = Serial(port=ports[0], baudrate=115200)
ser.flushInput()

comp_list = ["arduino->pi end", "arduino->pi"]
while True:
	if ser.inWaiting() > 0:
		inputValue = ser.readline().decode("utf-8").strip()
		print(inputValue)
		if inputValue in comp_list:
			try:
				n = input("Set arduino flash times:")
				if n == "exit":
					exit()

				message = "{}".format(n)
				to_write = bytearray(message.encode("ascii"))
				ser.write(to_write)
			except:
				print("Input error, please input a number")
				message = "{}".format(0)
				to_write = bytearray(message.encode("ascii"))
				ser.write(to_write)
