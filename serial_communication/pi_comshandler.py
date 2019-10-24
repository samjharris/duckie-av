import serial
import serial.tools.list_ports as list_ports

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