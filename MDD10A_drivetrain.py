from RPi import GPIO
from time import sleep
import time
#import keyboard

# P - Power Pin, D - Directional Pin
motor1Dir = 2;
motor1PWM = 3;
clk1 = 14;
dt1 = 15;

motor2Dir = 17;
motor2PWM = 27;
clk2 = 23;
dt2 = 24;

motor3Dir = 9;
motor3PWM = 10;
clk3 = 8;
dt3 = 7;

motor4Dir = 5;
motor4PWM = 6;
clk4 = 20;
dt4 = 21;

GPIO.setmode(GPIO.BCM);

GPIO.setup(motor1PWM, GPIO.OUT);
GPIO.setup(motor1Dir, GPIO.OUT);
GPIO.setup(motor2PWM, GPIO.OUT);
GPIO.setup(motor2Dir, GPIO.OUT);
GPIO.setup(motor3PWM, GPIO.OUT);
GPIO.setup(motor3Dir, GPIO.OUT);
GPIO.setup(motor4PWM, GPIO.OUT);
GPIO.setup(motor4Dir, GPIO.OUT);

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(clk4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(dt4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);

# Give full power to motor
GPIO.output(motor1PWM, GPIO.HIGH);
GPIO.output(motor1Dir, GPIO.HIGH);

GPIO.output(motor2PWM, GPIO.HIGH);
GPIO.output(motor2Dir, GPIO.HIGH);

GPIO.output(motor3PWM, GPIO.HIGH);
GPIO.output(motor3Dir, GPIO.HIGH);

GPIO.output(motor4PWM, GPIO.HIGH);
GPIO.output(motor4Dir, GPIO.HIGH);

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
