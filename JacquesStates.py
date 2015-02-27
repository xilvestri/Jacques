#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO

Status1="P8_11"
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"

Button= "P8_10"


GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)
GPIO.setup(Button, GPIO.IN)

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
    
    
def states (command):

    if command == "c":
        state= "Calibrate"
    elif command == "s":
        state = "Search"
    elif command == "p":
        state= "Position"
    elif command == "ro":
        state = "Roast"
    elif command == "re":
        state= "return"
    elif command == "o":
        state = "sleep"
    else:
        state = "none"
    
    return state
    
state =0
while (1):
#    command = raw_input("state? (c/s/p/ro/re):")
#    print state
    if GPIO.input(Button) == 1:
        state = buttonStatus(Button,state)
#    time.sleep(1)
