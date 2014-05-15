#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import search
import Adafruit_BBIO.UART as UART
import serial

Ultra3E="P9_16"
Ultra3T="P9_11"
Status5="P8_17"
SButton= "P8_10"

Status1="P8_11" 
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"

GPIO.setup(Ultra3E, GPIO.IN)
GPIO.setup(Ultra3T, GPIO.OUT)

GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)
GPIO.setup(SButton, GPIO.IN)

ADC.setup()

blinkCount=0

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

#=================return to Master================
#  Backs up until obstacle found. Stops and signals
#  mission success!
def returnToMaster(state):
    here=0                           #not back to master now
    blinkCount=0
    driveCom="F"
    ser.write(driveCom)
    
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
        
  
        if driveCom != "F":
            driveCom="F"
            ser.write(driveCom)
            
        SonarB = search.readSonar(Ultra3T, Ultra3E)
        if SonarB<=30:
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
            time.sleep(1.1)
            GPIO.output(Status1, GPIO.LOW)
            GPIO.output(Status2, GPIO.LOW)            
            GPIO.output(Status3, GPIO.LOW)
            GPIO.output(Status4, GPIO.LOW)
            GPIO.output(Status5, GPIO.LOW)
            
            here=1
        
        
        if (here== 1):
            state = 3     #allows for immediate state change to search state
            
    
    return state
