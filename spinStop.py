#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial
import numpy as np

import time


Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
Status1="P8_11"
Status2="P8_12"
Status3="P8_13"
Status4="P8_14"
Status5="P8_17"
SButton= "P8_10"
SeButton= "P8_18"
ADC.setup()
GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

ser.open()

#===============translate===============================================
#   Takes a number within an expected range, and maps it to another range
#   Found on stack exchage
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
    
#===============readFlames===============================================
#   Similar to the calibrate phase, takes an average of a set of readings and
#   provides that average as an overall reading. Alloes for a running average
#   to smooth out spiking readings
def readFlames(Flame1, Flame2, Flame3):
    sample1 = []
    sample2 = []
    sample3 = []
    full=[1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0]
    for x in range(0,10):
                
        #collect values of sensor
        Flame1reading = ADC.read_raw(Flame1)
        Flame2reading = ADC.read_raw(Flame2)
        Flame3reading = ADC.read_raw(Flame3)
        
        if Flame1reading < 1780.0:        
            sample1 = sample1 + [Flame1reading]
        if Flame2reading < 1780.0:
            sample2 = sample2 + [Flame2reading]
        if Flame3reading < 1780.0:
            sample3 = sample3 + [Flame3reading]

            
    #eliminate outliers if found
    sample1=[e for e in sample1 if (np.median(sample1)-2*np.std(sample1) < e <np.median(sample1) +2 * np.std(sample1))]
    if len(sample1)==0:
        sample1=full
    sample2=[e for e in sample2 if (np.median(sample2)-2*np.std(sample2) < e <np.median(sample2) +2 * np.std(sample2))]
    if len(sample2)==0:
        sample2=full
    sample3=[e for e in sample3 if (np.median(sample3)-2*np.std(sample3) < e <np.median(sample3) +2 * np.std(sample3))]
    if len(sample3)==0:
        sample3=full
            
    #takes average of values and stores for future use.
    read1 = np.mean(sample1)
    read2 = np.mean(sample2)
    read3 = np.mean(sample3)
    
    return {'FlameRead1':read1, 'FlameRead2':read2, 'FlameRead3':read3}
    
def spinStop(driveCom, minAll, max1, max2, max3):
    blinkCount=0
    count = 0
    spin=0                         #if program called, Jacques currently not centered
    while(spin==0):                #while not centered
        
        #wait for readings to level out 
        if driveCom!="D":
            time.sleep(.4)
        #read flame sensors
        Flame1reading = ADC.read_raw(Flame1)
        Flame2reading = ADC.read_raw(Flame2)
        Flame3reading = ADC.read_raw(Flame3)
        ScaledFlame1=translate(Flame1reading, minAll, max1, 5, 100)
        ScaledFlame2=translate(Flame2reading, minAll, max2, 5, 100)
        ScaledFlame3=translate(Flame3reading, minAll, max3, 5, 100)
        lowestFlame = min(ScaledFlame1, ScaledFlame2, ScaledFlame3)
        
        #Check to be sure flame is, in fact, not centered
        # if(lowestFlame>100):
        #     driveCom="D"
        #     ser.write(driveCom)
        #     driveCom="G"
        #     ser.write(driveCom)
        #     time.sleep(.8)
        if lowestFlame >90:                               #Determine speed of robot based on perceived distance
            newDrive="D"
        elif lowestFlame<=90:
            newDrive="G"
        if (newDrive !=driveCom):
            driveCom=newDrive
            ser.write(driveCom)

        
        if(lowestFlame != ScaledFlame2) and lowestFlame<=90:
            if (ScaledFlame3 == lowestFlame):
                driveCom="d"    #turn right
                ser.write(driveCom)

            else:
                driveCom="e"             #turn left
                ser.write(driveCom)
        
        #if flame is cetered and it isn't stopped
        if(lowestFlame==ScaledFlame2  and lowestFlame<=90 and driveCom!="G"):
            driveCom="G"
            ser.write(driveCom)
            spin=1        #flame centered
        
        #if flame is cetered and it is stopped
        elif(lowestFlame==ScaledFlame2 and lowestFlame<=90 and driveCom=="G"):
            spin=1
        
    return spin            # centered?
        
    GPIO.cleanup()
    
driveCom="G"
minAll=200
max1=1780
max2=1780
max3=1780
while 1:
    spin=spinStop(driveCom, minAll, max1, max2, max3)
 