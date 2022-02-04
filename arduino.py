import serial, time 

              
def comm_arduino(msg):
	with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
		time.sleep(0.1)
		if arduino.isOpen():
			arduino.write(msg.encode())
			while arduino.inWaiting()==0: pass
			if arduino.inWaiting()>0:
				answer=arduino.readline()
				print(answer)
				arduino.flushInput()
		
