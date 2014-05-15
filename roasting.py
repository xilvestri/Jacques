#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import Adafruit_BBIO.UART as UART
import serial
import Adafruit_BBIO.PWM as PWM

motorPWM= "P8_19"
motorA="P8_20"
motorB="P8_21"
pot = "P9_33"

GPIO.setup(motorA,GPIO.OUT)
GPIO.setup(motorB,GPIO.OUT)

Status1="P8_11"
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"

GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)

Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
Status4="P8_14"
RButton= "P8_18"
SButton= "P8_10"
probe = 'P9_37'
ADC.setup()

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

#=================roasting===============================
#  listens for thermoprobe value. After set time, sets LEDs
#  to signal the roast has failed
def roasting(state):
    blinkCount=0
    timeStart=time.time()
    while state == 8:
        if(blinkCount<=700):
             GPIO.output(Status4, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(700<blinkCount<=1400):
             GPIO.output(Status4, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
            
        reading = ADC.read_raw(probe)

        if (reading> 1420):
            # Position servo in up position
            state = 10     #allows for immediate state change to return state
            servoCom="Y"                #set servo to start position
            ser.write(servoCom)
            
            #stop the mallow!
            #GPIO.output(motorA, GPIO.LOW)
            #GPIO.output(motorB, GPIO.LOW)
            #PWM.set_duty_cycle(motorPWM, (0))
            GPIO.output(Status4, GPIO.LOW)
            # pinMallow="b"                   #stop the mallow!
            # ser.write(spinMallow)
            
        if (GPIO.input(SButton) == 1):
            state=9        #brings to pause state for manual advance
        
        timeNow=time.time()
        timePass=timeNow-timeStart
        if timeStart > 120 and reading<1370:
            while(state==8):
                GPIO.output(Status1, GPIO.HIGH)
                GPIO.output(Status2, GPIO.LOW)            #LED pattern for failed roast
                GPIO.output(Status3, GPIO.HIGH)
                GPIO.output(Status4, GPIO.LOW)
                GPIO.output(Status5, GPIO.HIGH)
                if (GPIO.input(SButton) == 1):
                    state=7        #brings to pause state for manual advance
            
    
    return state
