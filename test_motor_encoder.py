from RPi import GPIO
from time import sleep
import time
#import keyboard

motor1L = 2;
motor1R = 3;
clk1 = 14;
dt1 = 15;

motor2L = 17;
motor2R = 27;
clk2 = 23;
dt2 = 24;

motor3L = 9;
motor3R = 10;
clk3 = 8;
dt3 = 7;

motor4L = 5;
motor4R = 6;
clk4 = 20;
dt4 = 21;

GPIO.setmode(GPIO.BCM);

GPIO.setup(motor1L, GPIO.OUT);
GPIO.setup(motor1R, GPIO.OUT);
GPIO.setup(motor2L, GPIO.OUT);
GPIO.setup(motor2R, GPIO.OUT);
GPIO.setup(motor3L, GPIO.OUT);
GPIO.setup(motor3R, GPIO.OUT);
GPIO.setup(motor4L, GPIO.OUT);
GPIO.setup(motor4R, GPIO.OUT);

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);

# Give full power to motor
GPIO.output(motor1L, GPIO.HIGH); 
GPIO.output(motor1R, GPIO.LOW);   

GPIO.output(motor2L, GPIO.LOW); 
GPIO.output(motor2R, GPIO.HIGH);   

GPIO.output(motor3L, GPIO.LOW); 
GPIO.output(motor3R, GPIO.LOW);   

GPIO.output(motor4L, GPIO.LOW); 
GPIO.output(motor4R, GPIO.LOW);   

global encoderVal, encoderPPM, storedTime, currTime, shaftRPM, gearboxRPM
storedTime = [-1, -1, -1, -1]
encoderVal = [0, 0, 0, 0]
encoderPPM = 11
shaftRPM = [0, 0, 0, 0]
gearboxRPM = [0, 0, 0, 0]

def encoderInit(channel):
	global encoderVal, encoderPPM, storedTime, currTime, shaftRPM, gearboxRPM
	encoderVal[0]=encoderVal[0]+1;
	currTime = time.time()
	#print("Pulse!")
	
	if storedTime[0] == -1:
		storedTime[0] = time.time()
	else:
		timeDiff = currTime - storedTime[0]
		storedTime[0] = currTime
		timeFactor = 60/timeDiff
		
		shaftRPM[0] = encoderVal[0]*timeFactor / encoderPPM;
		gearboxRPM[0] = shaftRPM[0]/40
		
		encoderVal[0] = 0

	
GPIO.add_event_detect(dt1,GPIO.RISING, callback=encoderInit)

interval = 1
try:  
	while True:
		if shaftRPM[0] != 0 and gearboxRPM[0] != 0:		
			print("Gearbox RPM:",gearboxRPM[0]," | Shaft RPM:",shaftRPM[0])
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	GPIO.cleanup()                 # resets all GPIO ports used by this program  

