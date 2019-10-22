import serial.tools.list_ports as list_ports
from serial import Serial
from time import sleep

# connect to the open serial port
ports = list(list_ports.comports())
ports = [p[0] for p in ports]
print(ports)

