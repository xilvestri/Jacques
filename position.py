#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time


Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
thermistor = "P9_39"
Status3="P8_13"
SButton= "P8_10"
ADC.setup()



def position(state, maxTherm, minTherm):
    blinkCount=0
    blinkTime=runBlink
    
    spinMallow=0                   #spin the mallow!
    ser.write(spinMallow)
    time.sleep(.2)
    servoCom="Y"                #set servo to start position
    ser.write(servoCom) 
    
    while state == 6:
        if (GPIO.input(SButton) == 1):
            state = 7                                #return a state of 7 so manual state control can occur
            
        if(blinkCount<=blinkTime):
            GPIO.output(Status2, GPIO.HIGH)
            blinkCount = blinkCount+1
        elif(blinkTime<blinkCount<=(blinkTime*2)):
            GPIO.output(Status2, GPIO.LOW)
            blinkCount = blinkCount +1
            else:
            blinkCount=0
            
        
        servoCom="Z"                    #move servo down (3) degrees 
        ser.write(servoCom)
        
        
        #reads thermistor to check quality of position
        time.sleep(.6)
        thermistor=ADC.read_raw(thermistor)
        
        #if thermistor angle is where we want it
        if(thermistor>((maxTherm+minTherm)*2/3)):
            state = 8    #allows for immediate state change to roasting
            
        servoState=ser.read()           #reads in current servo position
        elif (servoState >= 90):
            servoCom="Y"                #set servo to start position
            ser.write(servoCom)     
            startCount=startCount +1    #try again?
            if startCount==2:           #go back to search
                state=4
            
    
    return state
        
