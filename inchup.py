#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial

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

Ultra1E="P9_15"
Ultra1T="P9_13"
Ultra2E="P9_27"
Ultra2T="P9_25"
Ultra3E="P8_16"
Ultra3T="P8_15"
Ultra4E="P9_16"
Ultra4T="P9_11"

GPIO.setup(Status1, GPIO.OUT)
GPIO.setup(Status2, GPIO.OUT)
GPIO.setup(Status3, GPIO.OUT)
GPIO.setup(Status4, GPIO.OUT)
GPIO.setup(Status5, GPIO.OUT)

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

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
    
def readSonar(sensorTrig, sensorEcho):
    
    signaloff=0
    while(signaloff==0):
        time.sleep(.01)
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

def center(driveCom, minAll, max1, max2, max3):
    blinkCount=0
    count = 0
    centered=0                         #if program called, Jacques currently not centered
    while(centered==0):                #while not centered
            
        time.sleep(.3)
        Flame1reading = ADC.read_raw(Flame1)
        Flame2reading = ADC.read_raw(Flame2)
        Flame3reading = ADC.read_raw(Flame3)
        ScaledFlame1=translate(Flame1reading, minAll, max1, 5, 100)
        ScaledFlame2=translate(Flame2reading, minAll, max2, 5, 100)
        ScaledFlame3=translate(Flame3reading, minAll, max3, 5, 100)
        lowestFlame = min(ScaledFlame1, ScaledFlame2, ScaledFlame3)

        
        #Check to be sure flame is, in fact, not centered
        if(lowestFlame != ScaledFlame2):
            if (ScaledFlame3 == lowestFlame):
                GPIO.output(Status1, GPIO.HIGH)
                driveCom="d"    #turn left
                ser.write(driveCom)

            else:
                driveCom="e"             #turn right
                GPIO.output(Status5, GPIO.HIGH)
                ser.write(driveCom)


            
        elif(lowestFlame==ScaledFlame2 and driveCom!="G"):
            driveCom="G"
            ser.write(driveCom)
            #print str(driveCom)
            centered=1        #flame centered
        
    return centered             # centered?
        
    GPIO.cleanup()
    
def inchUp(position):
    ready=0
    while (position==0):
        centered = center(driveCom, 130, 1799, 1799, 1799)          #Centering up robot
        count=0
        if centered ==1:
            while count<4:
                time.sleep(.3)
                SonarC = readSonar(Ultra2T, Ultra2E)       #inch up to flame stand
                if (SonarC<12-1):
                    driveCom="f"
                    ser.write(driveCom)
                    ready=0
                elif (SonarC>1+14):
                    driveCom="c"
                    ser.write(driveCom)
                    ready=0
                elif(driveCom!="G"):
                    driveCom="G"
                    ser.write(driveCom)
                    ready=ready+1
                count=count+1
        if (ready>3):
            position=1  
    
    return position

centered=0



while(1):
    position=0
    position=inchUp(position)
    #if position=1:
    print position
