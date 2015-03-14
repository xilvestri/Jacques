#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO
import calibration
import search
import position
import roasting
import returnToMaster


#---------Status LEDs---------
Status1="P8_11" 
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"

#--------State Button---------
#Controls state manually for testing or emergency
SButton= "P8_10"


GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)
GPIO.setup(SButton, GPIO.IN)

#LEDs start Low
GPIO.output(Status1, GPIO.LOW)
GPIO.output(Status2, GPIO.LOW)
GPIO.output(Status3, GPIO.LOW)
GPIO.output(Status4, GPIO.LOW)
GPIO.output(Status5, GPIO.LOW)


# Reads StateButton and switches between states in two second intervals
#state 0 =sleep/restart 
#state 2 =calibrate
#state 4 =search
#state 6 =position
#state 8 =roast
#state 10=return
#state 12=end/sleep

def buttonStatus(buttonPin,state):    #takes in the button pin number and the current state of the robot
    
    signalon = time.time()        #reads in time of button press
    signaloff = 0                 #initializes off command. 
    
    while signaloff ==0:                             #loop continues until button released
        signalnow= time.time()                       #gets current length of button press
        
        if state == 12:                              #if previously coming out of a sleep state/end of program, restart 
            state =0
            
        length= signalnow-signalon + state           #adds state to current length of button press. Insures count 
                                                     #continues through to the next state 
                                                     
        if length<=.1:                               #short button press to  account for signal spikes or mis-hits
            command= 0
#            print "restart"

        elif length <=2:                             #Calibration phase entered. Lights corresponding state light up.
            command= 2                               #Stores a command for the exit state.
#            print "calibrate"
            GPIO.output(Status1, GPIO.HIGH)

        elif length <= 4:                            #Search phase entered. Lights corresponding state light up.
            command = 4                              #Stores a command for the exit state.
#            print "search"
            GPIO.output(Status1, GPIO.LOW)
            GPIO.output(Status2, GPIO.HIGH)

        elif length <= 6:                            #position phase entered. Lights corresponding state light up.
            command = 6                              #Stores a command for the exit state.
#            print "position"
            GPIO.output(Status2, GPIO.LOW)
            GPIO.output(Status3, GPIO.HIGH)

        elif length <= 8:                            #roast phase entered. Lights corresponding state light up.
            command = 8                              #Stores a command for the exit state.
#            print "roast"
            GPIO.output(Status3, GPIO.LOW)
            GPIO.output(Status4, GPIO.HIGH)

        elif length <= 10:                            #return phase entered. Lights corresponding state light up.
            command = 10                              #Stores a command for the exit state.
#            print "return"
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.HIGH)
        elif length >10:                              #end phase entered. Lights corresponding state light up.
            command = 12                              #Stores a command for the exit state.
#            print "off"
            GPIO.output(Status5, GPIO.LOW)
            
        if GPIO.input(buttonPin) == 0:                #sets a buttonOff time that exits the loop
            signaloff= time.time()

    return command
    
    
state =0
while (1):
#    print state
    if GPIO.input(SButton) == 1:              # Launch manual state change
        state = buttonStatus(SButton,state)   #state 0=sleep, 2 = calibrate, 4 = search, 6 = position, 8=roast, 10 = return, 12=off, if button hit while sleep, will restart count and calibrate
#    time.sleep(1)
    if state ==2:
        GPIO.output(Status1, GPIO.HIGH)
       # print "calibration begun"
        Cresult = calibration.calibration(state) # returns: 'state':state, 'maxVal1': noAverage1, 'maxVal2':noAverage2,'maxVal3': noAverage3,'minVal1': yesAverage1,'minVal2': yesAverage2,'minVal3': noAverage3
        state= Cresult['state']
        max1= Cresult['maxVal1']
        max2= Cresult['maxVal2']           #Collect average flame sensor readings for the particular environment
        max3= Cresult['maxVal3']
        minAll= Cresult['minVal']
        maxTherm = Cresult['maxTherm']
        minTherm = Cresult['minTherm']
        print maxTherm
        print minTherm
        
        time.sleep(1)
        
        #Search for flame until centered in front of robot
    if state == 4:
        GPIO.output(Status1, GPIO.LOW)
        GPIO.output(Status2, GPIO.HIGH)
        #print "searching for flame"
        state=search.search(state, max1, max2, max3, minAll)
        time.sleep(1)
        
        #Position marshmallow in roasting position over flame. End phase when properlly located
    if state == 6:
        GPIO.output(Status2, GPIO.LOW)
        GPIO.output(Status3, GPIO.HIGH)
        #print "positioning marshmallow"
        state=position.position(state, maxTherm, minTherm)
        time.sleep(1)
        
        #roast marshmallow. End phase when core temperature reached
    if state == 8:
        GPIO.output(Status3, GPIO.LOW)
        GPIO.output(Status4, GPIO.HIGH)
        print "roasting in progress"
        #state= roasting.roasting(state)
        time.sleep(1)
        
        #Return to master. End phase when arrived at master.
    if state == 10:
        GPIO.output(Status4, GPIO.LOW)
        GPIO.output(Status5, GPIO.HIGH)
        print "roast complete, return now"
        time.sleep(1)
        
        #End Program, enter sleep mode. 
    if state == 12:
        GPIO.output(Status5, GPIO.LOW)
        print "sleep mode"
