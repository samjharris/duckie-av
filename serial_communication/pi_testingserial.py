from pi_serial import SerialCon 
import time

##Initialize serial communication
sc = SerialCon()
ports = sc.getOpenPorts()
if not ports:
	print("No open serial ports, exiting")
	exit()
#Select & set appropriate port
port = ports[0]
sc.setPort(port)
#Set appropriate baud rate
sc.setBaud(115200)
#Initialize the connection
sc.initConnection()


x = 0
while (True):
	sc.write(x)
	x+=1
	time.sleep(1)
	