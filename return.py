#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import search

Status5="P8_17"
SButton= "P8_10"
ADC.setup()

blinkCount=0

def returnToMaster(state):
    here=0                           #not back to master now
    blinkCount=0
    
    while state == 10:
        if(blinkCount<=700):
            GPIO.output(Status5, GPIO.HIGH)
            blinkCount = blinkCount+1
        elif(700<blinkCount<=1400):
            GPIO.output(Status5, GPIO.LOW)
            blinkCount = blinkCount +1
        else:
            blinkCount=0
            
        if (GPIO.input(SButton) == 1):
            state=13        #brings to pause state for manual advance
        
   
        #Put return code here
        driveCom="F"
        ser.write(driveCom)
        SonarR = search.readSonar(Ultra1T, Ultra1E)
        if SonarR<=20:
            driveCom="G"
            ser.write(driveCom)
            GPIO.output(Status1, GPIO.HIGH)
            GPIO.output(Status2, GPIO.LOW)            #LED pattern for mission success
            GPIO.output(Status3, GPIO.HIGH)
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.HIGH)
            time.sleep(1.1)
            GPIO.output(Status1, GPIO.LOW)
            GPIO.output(Status2, GPIO.HIGH)            
            GPIO.output(Status3, GPIO.LOW)
            GPIO.output(Status4, GPIO.HIGH)
            GPIO.output(Status5, GPIO.LOW) 
            time.sleep(1.1)
            GPIO.output(Status1, GPIO.HIGH)
            GPIO.output(Status2, GPIO.LOW)            
            GPIO.output(Status3, GPIO.HIGH)
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.HIGH)
            time.sleep(1.1)
            GPIO.output(Status1, GPIO.LOW)
            GPIO.output(Status2, GPIO.HIGH)            
            GPIO.output(Status3, GPIO.LOW)
            GPIO.output(Status4, GPIO.HIGH)
            GPIO.output(Status5, GPIO.LOW) 
            time.sleep(1.1)
            GPIO.output(Status1, GPIO.HIGH)
            GPIO.output(Status2, GPIO.LOW)            
            GPIO.output(Status3, GPIO.HIGH)
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.HIGH)
            
            here=1
        
        
        if (here== 1):
            state = 12     #allows for immediate state change to return state
            
    
    return state
