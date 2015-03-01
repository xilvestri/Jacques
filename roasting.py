#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time


Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
Status4="P8_14"
RButton= "P8_18"
ADC.setup()

Cflag = 0
blinkCount=0

def roasting(state):
    Cflag = 0
    blinkCount=0
    while state == 8:
        if(blinkCount<=700):
             GPIO.output(Status4, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(700<blinkCount<=1400):
             GPIO.output(Status4, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
        
        if (GPIO.input(RButton) == 1 and Cflag == 0):
            print "Roasting Roasting Roasting"
            time.sleep(2)
            print "Yummy :)"
            #Put real positioning code here
            state = 10
            
    
    return state
        
