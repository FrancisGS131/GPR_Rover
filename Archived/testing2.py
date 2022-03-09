from RPi import GPIO
from time import sleep
import time

motorL = 23;
motorR = 24;
clk = 8;
dt = 7;

GPIO.setmode(GPIO.BCM);
GPIO.setup(motorL, GPIO.OUT);
GPIO.setup(motorR, GPIO.OUT);
GPIO.output(motorL, GPIO.HIGH); # set GPIO23 to 1/GPIO.HIGH/True  
GPIO.output(motorR, GPIO.LOW); # set GPIO24 to 0/GPIO.LOW/False  

GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);

global counter
counter = 0;
clkLastState= GPIO.input(clk);

def detectDir(channel):
	global counter
	clkState = GPIO.input(clk)
	dtState = GPIO.input(dt)
	
	#print(clkState,clkLastState)
	if clkState!=clkLastState and clkState==1:
		#print("entered")
		if dtState != clkState:
			counter+=1
			#print(counter,"CW")
		else:
			counter-=1
			#print(counter,"CCW")
			
	clkLastState = clkState;
	#sleep(0.0)

timeStamp = time.time()
interval = 1
try:  
	while True:
		currTime = time.time()
		#print(currTime-timeStamp)
		
		clkState = GPIO.input(clk)
		dtState = GPIO.input(dt)
		
		#print(clkState,clkLastState)
		if clkState!=clkLastState and clkState==1:
			#print("entered")
			if dtState != clkState:
				counter+=1
				#print(counter,"CW")
			else:
				counter-=1
				#print(counter,"CCW")
				
		clkLastState = clkState;
		#sleep(0.0)
		
		if currTime-timeStamp > interval:
			timeStamp = currTime;
			print("Pulses in 1 second:",counter)
			rpm = counter*60 / 11;
			print(counter,"pulses/11"," pulse per rotation * 60s=",rpm," RPM at shaft")
			print("Gearbox RPM is RPM above/40:",rpm/40)
			counter = 0;
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	GPIO.cleanup()                 # resets all GPIO ports used by this program  

