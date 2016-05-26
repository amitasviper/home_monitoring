import serial 
import Adafruit_BBIO.UART as UART
UART.setup("UART1")
DATA= serial.Serial( '/dev/ttyO1',9600)
while(1):
	while DATA.inWaiting()==0:
		pass	
	NMEA=DATA.readline()
	print NMEA

