import RPi.GPIO as GPIO
import time
from datetime import datetime
GPIO.setmode(GPIO.BCM)

input_A = 18
input_B = 23

lastEncoded = 0
encoderValue = 0

#Interrup Service Routine
def updateEncVal(channel):
    global  lastEncoded, encoderValue
    MSB = GPIO.input(input_A)
    LSB = GPIO.input(input_B)
    encoded = (MSB << 1)| LSB
    suma  = (lastEncoded << 2) | encoded 
    if suma == 13 or suma == 4 or suma == 2 or suma == 11:
        encoderValue = encoderValue +1
    if suma == 14 or suma == 7 or suma == 1 or suma == 8:
        encoderValue= encoderValue -1
    lastEncoded = encoded

#GPIO Setup
GPIO.setup(input_A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(input_B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Attach interrupt
GPIO.add_event_detect(input_A, GPIO.BOTH, callback = updateEncVal)
GPIO.add_event_detect(input_B, GPIO.BOTH, callback = updateEncVal)

#Log data to txt file
f = open("/media/pi/HD/logenc/" + time.strftime("%d_%m_%Y_%H_%M") + '.txt','w+')

while True:
    print("Encoder Value: " + str(encoderValue) + "  Metros:"+ str((encoderValue*0.3330096)/800))
    f.write(datetime.now().strftime('%H%M%S.%f') + " , " + str(encoderValue) + " , "+ str((encoderValue*0.3330096)/800)+ "\n")
    time.sleep(0.1)


