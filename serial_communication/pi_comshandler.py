import serial
import serial.tools.list_ports as list_ports
import struct
import time
import sys
sys.path.append('../pi')
import ticks_to_distance as ticks_to_distance

<<<<<<< HEAD
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

comp_list = ["Motor Values? Pi\r\n"]
##begin control loop
while True:
	if s_con.inWaiting() > 0:

		inputValue = s_con.readline()

		
		# n = input("Set arduino flash times:")
		print(inputValue)
		if inputValue in comp_list:
			try:
				right_value = 20
				left_value = 50

				s_con.write(struct.pack('>BB', right_value, left_value))
			except:
				print("error passing motor values")
				s_con.write('0')


		if len(inputValue.split()) != 2:
			continue

		love = inputValue.strip()
		left_ticks, right_ticks = [int(x) for x in love.split()]
		# print(left_ticks, right_ticks)

		left_distance, right_distance = ticks_to_distance.get_distances(left_ticks, right_ticks)
		print("distances: ", left_distance, right_distance)

		time.sleep(0.2)


def sendData(data):
	return
=======
##Serial connection object definition
class SerialCon():
	def __init__(self):
		self.baud_rate=115200
		self.port=None
		self.sc=None

	##Set the baud rate
	def setBaud(self,baud):
		self.baud_rate=baud
		return

	##Set the port
	def setPort(self,new_port):
		self.port=new_port
		return

	##Return a list of open ports
	def getOpenPorts(self):
		ports=list(list_ports.comports())
		ports=[p[0] for p in ports]
		return ports

	##Initialize the serial connection
	def initConnection(self):
		self.sc=serial.Serial(self.port,self.baud_rate)
		self.sc.flushInput()
		#todo:handlefailure?
		return

	##Read data from the serial port
	def write(self,data):
		self.sc.write(data)
		#todo:handleerrors
		return

	##Write data to the serial port
	def read(self):
		data=self.sc.read(self.sc.inWaiting())
		#readgetsonebyte,readLinegetsline
		#todo:whentherewasnodata,orbusy,doesthisreturnNull?Weshouldhandlethis
		return data

##Usage example
mySerial=SerialCon()
ports=mySerial.getOpenPorts() #if this list is empty, no open ports
mySerial.setPort(ports[0])
mySerial.setBaud(115200)
mySerial.initConnection()

x=0
y=0
x=mySerial.read()
mySerial.write(y)
>>>>>>> a27915ed0569e9b0a0f86712197b4d6153727822
