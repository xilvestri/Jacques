#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import serial
import Adafruit_BBIO.PWM as PWM


motorPWM= "P8_19"
motorA="P8_20"
motorB="P8_21"
pot = "P9_33"

GPIO.setup(motorA,GPIO.OUT)
GPIO.setup(motorB,GPIO.OUT)

PWM.start(motorPWM,0, 500)


Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
thermistor = "P9_39"
Status3="P8_13"
SButton= "P8_10"
ADC.setup()

ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

ser.open()


def position(state, Status3,  minTherm):
    blinkCount=0
    startCount =0
    servoCount =0
    thermistor="P9_39"
    
    #spin the mallow!
    #potVal=ADC.read(pot)
    #GPIO.output(motorA, GPIO.HIGH)
    #GPIO.output(motorB, GPIO.LOW)
    #PWM.set_duty_cycle(motorPWM, (100*potVal ))
    
    time.sleep(.2)
    servoCom="Y"                #set servo to start position
    ser.write(servoCom) 
    
    while state == 6:
        if (GPIO.input(SButton) == 1):
            state = 7                                #return a state of 7 so manual state control can occur
            
        if(blinkCount<=1):
            GPIO.output(Status3, GPIO.HIGH)
            blinkCount = blinkCount+1
        elif(1<blinkCount<=3):
            GPIO.output(Status3, GPIO.LOW)
            blinkCount = blinkCount +1
        else:
            blinkCount=0
            
        
        servoCom="W"                    #move servo down (6) degrees 
        ser.write(servoCom)
        
        
        #reads thermistor to check quality of position
        time.sleep(.35)
        thermistor=ADC.read_raw("P9_39")
        
        servoCount = servoCount +1
        
        #if thermistor angle is where we want it
        if(thermistor>(60+minTherm)):
            servoCom="W"                    #move servo down (6) degrees 
            ser.write(servoCom)
            state = 8    #allows for immediate state change to roasting
         
        
        elif (servoCount >= 28):
            servoCount =0
            servoCom="Y"                #set servo to start position
            ser.write(servoCom)     
            startCount=startCount +1    #try again?
            if startCount==2:           #go back to search
                GPIO.output(Status3, GPIO.LOW)
                state=4
            
    
    return state
