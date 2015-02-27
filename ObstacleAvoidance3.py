#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial
import random

state ="NotCentered"

Ultra1E="P9_15"
Ultra1T="P9_11"
Ultra2E="P9_27"
Ultra2T="P9_25"
Ultra3E="P8_16"
Ultra3T="P8_15"
Ultra4E="P9_16"
Ultra4T="P9_13"

GPIO.setup(Ultra1E, GPIO.IN)
GPIO.setup(Ultra1T, GPIO.OUT)
GPIO.setup(Ultra2E, GPIO.IN)
GPIO.setup(Ultra2T, GPIO.OUT)
GPIO.setup(Ultra3E, GPIO.IN)
GPIO.setup(Ultra3T, GPIO.OUT)
GPIO.setup(Ultra4E, GPIO.IN)
GPIO.setup(Ultra4T, GPIO.OUT)

GPIO.output(Ultra1T, GPIO.LOW)
GPIO.output(Ultra2T, GPIO.LOW)
GPIO.output(Ultra3T, GPIO.LOW)
GPIO.output(Ultra4T, GPIO.LOW)

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

ser.open()

def readSonar(sensorTrig, sensorEcho):
    time.sleep(.01)
    signaloff=0
    while(signaloff==0):
        GPIO.output(sensorTrig, True)
        time.sleep(0.00001)
        GPIO.output(sensorTrig, False)
        
        while GPIO.input(sensorEcho) == 0:
            signaloff = time.time()
            
        while GPIO.input(sensorEcho) == 1:
            signalon= time.time()
        
    timepassed = signalon - signaloff
        
    distance = timepassed *17000
    
    return distance
        
    GPIO.cleanup()
    
driveCom = "C"
ser.write(driveCom)
count = 0
x =0

for x in range(0,200):
    
    SonarR = readSonar(Ultra1T, Ultra1E)
    SonarL= readSonar(Ultra3T, Ultra3E)
    SonarC = readSonar(Ultra2T, Ultra2E)
    SonarB = readSonar(Ultra4T, Ultra4E)
    lowest= min(SonarR, SonarL, SonarC, SonarB)
    
#    print "right: " + str(SonarR)
#    print "left: " + str(SonarL)
#    print "center: " + str(SonarC)
#  print "back: " + str(SonarB)
    if lowest <= 25:
         #if (not ((driveCom == "F" and SonarB!= lowest) or (driveCom == "C" and SonarB==lowest))):
         driveCom="G"
         #print "Stop!!!!"

         ser.write(driveCom)
         time.sleep(.5)
         if SonarB != lowest:
             driveCom= "F"       #reverse drive
             ser.write(driveCom)
          #   print str(driveCom)
             count = 1
             while count<= 30:
                 count = count+ random.randint(0,3)
                 SonarB = readSonar(Ultra4T, Ultra4E)
                 if SonarB <=15:
                     driveCom="G"
                     ser.write(driveCom)
                     count = 35
             driveCom=random.choice([ "D", "E"]) #forward turn right, forward turn left
             ser.write(driveCom)
#             print str(driveCom)
             count = 1
         
         else:
             driveCom= "C"
             count = 1
#             print str(driveCom)
             ser.write(driveCom)
             while count<= 60:
                 count = count+ random.randint(0,3)
                 SonarR = readSonar(Ultra1T, Ultra1E)
                 SonarL= readSonar(Ultra3T, Ultra3E)
                 SonarC = readSonar(Ultra2T, Ultra2E)
                 if SonarR <=20 or SonarL<=20 or SonarC <=20:
                     driveCom="G"
                     ser.write(driveCom)
                     count = 65
             driveCom=random.choice([ "D", "E"]) #forward turn right, forward turn left
             ser.write(driveCom)
 #            print str(driveCom)
             count = 1
         
    if (driveCom== "D" or "E"):
        if(1<=count <=70):
            count = count+ random.randint(0,3)
        if(count >70):
           driveCom= "C"
#           print str(driveCom)
           ser.write(driveCom)
           count = 0 
    
    else:
#        print str(driveCom)
        ser.write(driveCom)
#    x=x+1
#    print str(x) +  "  " + str(lowest)
driveCom = "G"
ser.write(driveCom)
GPIO.cleanup
