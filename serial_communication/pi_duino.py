import serial
import serial.tools.list_ports as list_ports


# connect to the open serial port
ports = list(list_ports.comports())
ports = [p[0] for p in ports]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
print("ports: {}".format(ports))

baud_rate = 9600


s1 = serial.Serial(ports[0], baud_rate)
s1.flushInput()

comp_list = ["Flash complete\r\n", "Hello Pi, This is Arduino UNO...\r\n"]
while True:
	if s1.inWaiting() > 0:
		inputValue = s1.readline()
		print(inputValue)
		if inputValue in comp_list:
			try:
				n = input("Set arduino flash times:")
				s1.write('%d' % n)
			except:
				print("Input error, please input a number")
				s1.write('0')

