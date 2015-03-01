#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO
import calibration
import search

Status1="P8_11"
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"

SButton= "P8_10"


GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)
GPIO.setup(SButton, GPIO.IN)

GPIO.output(Status1, GPIO.LOW)
GPIO.output(Status2, GPIO.LOW)
GPIO.output(Status3, GPIO.LOW)
GPIO.output(Status4, GPIO.LOW)
GPIO.output(Status5, GPIO.LOW)

def buttonStatus(buttonPin,state):
    signalon = time.time() 
    signaloff = 0
    while signaloff ==0:
        signalnow= time.time()
        if state == 12:
            state =0
        length= signalnow-signalon + state
        if length<=.1:
            command= 0
#            print "restart"

        elif length <=2:
            command= 2
#            print "calibrate"
            GPIO.output(Status1, GPIO.HIGH)

        elif length <= 4:
            command = 4
#            print "search"
            GPIO.output(Status1, GPIO.LOW)
            GPIO.output(Status2, GPIO.HIGH)

        elif length <= 6:
            command = 6
#            print "position"
            GPIO.output(Status2, GPIO.LOW)
            GPIO.output(Status3, GPIO.HIGH)

        elif length <= 8:
            command = 8
#            print "roast"
            GPIO.output(Status3, GPIO.LOW)
            GPIO.output(Status4, GPIO.HIGH)

        elif length <= 10:
            command = 10
#            print "return"
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.HIGH)
        elif length >10:
            command = 12
#            print "off"
            GPIO.output(Status5, GPIO.LOW)
            
        if GPIO.input(buttonPin) == 0:
            signaloff= time.time()

    return command
    
    
state =0
while (1):
#    command = raw_input("state? (c/s/p/ro/re):")
#    print state
    if GPIO.input(SButton) == 1:
        state = buttonStatus(SButton,state)   #state 0=sleep, 2 = calibrate, 4 = search, 6 = position, 8=roast, 10 = return, 12=off, if button hit while sleep, will restart count and calibrate
#    time.sleep(1)
    if state ==2:
        GPIO.output(Status1, GPIO.HIGH)
        print "calibration begun"
        Cresult = calibration.calibration() # returns: 'state':state, 'maxVal1': noAverage1, 'maxVal2':noAverage2,'maxVal3': noAverage3,'minVal1': yesAverage1,'minVal2': yesAverage2,'minVal3': noAverage3
        state= Cresult['state']
        max1= Cresult['maxVal1']
        max2= Cresult['maxVal2']
        max3= Cresult['maxVal3']
        min1= Cresult['minVal1']
        min2= Cresult['minVal2']
        min3= Cresult['minVal3']
        
        time.sleep(1)
    if state == 4:
        GPIO.output(Status1, GPIO.LOW)
        GPIO.output(Status2, GPIO.HIGH)
        print "searching for flame"
        state=search.search(state, max1, max2, max3, min1, min2, min3)
        time.sleep(1)
    if state == 6:
        GPIO.output(Status2, GPIO.LOW)
        GPIO.output(Status3, GPIO.HIGH)
        print "positioning marshmallow"
        time.sleep(1)
    if state == 8:
        GPIO.output(Status3, GPIO.LOW)
        GPIO.output(Status4, GPIO.HIGH)
        print "roasting in progress"
        time.sleep(1)
    if state == 10:
        GPIO.output(Status4, GPIO.LOW)
        GPIO.output(Status5, GPIO.HIGH)
        print "roast complete, return now"
        time.sleep(1)

    if state == 12:
        GPIO.output(Status5, GPIO.LOW)
        print "sleep mode"
