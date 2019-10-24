import serial
import serial.tools.list_ports as list_ports

## connect to the open serial port
ports = list(list_ports.comports())
ports = [p[0] for p in ports]
if len(ports) == 0:
    print("error, couldn't find any open ports")
    exit()
print("found open ports: {}".format(ports))

## set the baud rate - this must match the uno's
baud_rate = 115200
#baud_rate = 9600

##initialize our serial connection
s_con = serial.Serial(ports[0], baud_rate)
s_con.flushInput()

comp_list = ["Flash complete\r\n", "Hello Pi, This is Arduino UNO...\r\n"]

##begin control loop
while True:

	##read data over serial while data is being written
	data = s_con.



	if s1.inWaiting() > 0:
		inputValue = s1.readline() #.read(n) reads n bytes
		print(inputValue)
		if inputValue in comp_list:
			try:
				n = input("Set arduino flash times:")
				s1.write('%d' % n)
			except:
				print("Input error, please input a number")
				s1.write('0')




def sendData(data):
	return

def 