#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO

#UltraE="P9_25" 
#UltraT="P9_27"
#UltraE="P9_15" 
#UltraT="P9_13"
#UltraE="P9_16"
#UltraT="P9_11"
UltraE="P8_16"
UltraT="P8_15"

GPIO.setup(UltraE, GPIO.IN)
GPIO.setup(UltraT, GPIO.OUT)
GPIO.output(UltraT, GPIO.LOW)


def readSonar(sensorTrig, sensorEcho):
    
    signaloff=0
    status=1
    while(signaloff==0):
        time.sleep(.01)
        GPIO.output(sensorTrig, True)
        time.sleep(0.00001)
        GPIO.output(sensorTrig, False)
        signalstart= time.time()
        
        while GPIO.input(sensorEcho) == 0 and status==1:
            signaloff = time.time()
            if (signaloff-signalstart) > .3:
                status=0
            
        while GPIO.input(sensorEcho) == 1 and status==1:
            signalon= time.time()
            if (signalon-signalstart) > .6:
                status=0
    
    if status==1:
        timepassed = signalon - signaloff
        distance = timepassed *17000
    if status==0:
        distance=0
        
    return distance
        
    GPIO.cleanup()
        
print (" ")
print readSonar(UltraT, UltraE)
