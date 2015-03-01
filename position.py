#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time


Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
Status3="P8_13"
PButton= "P8_18"
ADC.setup()

Cflag = 0
blinkCount=0

def position(state):
    Cflag = 0
    blinkCount=0
    while state == 6:
        if(blinkCount<=700):
             GPIO.output(Status3, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(700<blinkCount<=1400):
             GPIO.output(Status3, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
        
        if (GPIO.input(PButton) == 1 and Cflag == 0):
            print "Positioning positioning positioning"
            time.sleep(2)
            print "there ya go. Perfect! :)"
            #Put real positioning code here
            state = 8
            
    
    return state
        
