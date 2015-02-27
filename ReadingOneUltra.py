#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO

UltraE="P9_27" 
UltraT="P9_25"
#UltraE="P9_15" 
#UltraT="P9_11"
#UltraE="P9_16"
#UltraT="P9_13"
#UltraE="P8_16"
#UltraT="P8_15"

GPIO.setup(UltraE, GPIO.IN)
GPIO.setup(UltraT, GPIO.OUT)
GPIO.output(UltraT, GPIO.LOW)


def readSonar(sensorTrig, sensorEcho):
    
    signaloff=0
    while(signaloff==0):
        time.sleep(.01)
        GPIO.output(sensorTrig, True)
        time.sleep(0.00001)
        GPIO.output(sensorTrig, False)
        
        while GPIO.input(sensorEcho) == 0:
            signaloff = time.time()
            
        while GPIO.input(sensorEcho) == 1:
            signalon= time.time()
        
    timepassed = signalon - signaloff
        
    distance = timepassed *17000
    
    return distance
        
    GPIO.cleanup()
        
print (" ")
print readSonar(UltraT, UltraE)
