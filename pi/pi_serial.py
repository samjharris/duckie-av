##########################################################
# pi_serial.py                                           #
#                                                        #
#  This module implements using the rasppi to interface  #
# with the arduino via serial communication. Create a    #
# SerialCon object in a controller and use as such:      #
#                                                        #
#      Usage example:                                    #
# mySerial=SerialCon()                                   #
# ports=mySerial.getOpenPorts()                          #
# mySerial.setPort(ports[0])                             #
# mySerial.setBaud(115200)                               #
# mySerial.initConnection()                              #
#                                                        #
# x=0                                                    #
# y=0                                                    #
# x=mySerial.read()                                      #
# mySerial.write(y)                                      #
#                                                        #
##########################################################

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
		#todo:handle failure?
		return

	##Read data from the serial port
	def write(self,data):
		self.sc.write(data)
		#todo:handle errors
		return

	##Write data to the serial port
	def read(self):
		data=self.sc.read(self.sc.inWaiting())
		#read() gets one byte, readLine() gets line
		#todo: must handle when there was no data, or busy
		return data

