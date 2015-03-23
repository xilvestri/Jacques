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

Ultra1E="P9_15"
Ultra1T="P9_13"
Ultra2E="P9_27"
Ultra2T="P9_25"
Ultra3E="P8_16"
Ultra3T="P8_15"
Ultra4E="P9_16"
Ultra4T="P9_11"

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

normalBlink = 700
problemBlink = 400
runBlink = 1200


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def readSonar(sensorTrig, sensorEcho):
    start=time.time()
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
                #GPIO.output(Status1, GPIO.HIGH)
                driveCom="d"    #turn left
                ser.write(driveCom)

            else:
                driveCom="e"             #turn right
                #GPIO.output(Status5, GPIO.HIGH)
                ser.write(driveCom)


            
        elif(lowestFlame==ScaledFlame2 and driveCom!="G"):
            driveCom="G"
            ser.write(driveCom)
            #print str(driveCom)
            centered=1        #flame centered
        
        elif(lowestFlame==ScaledFlame2 and driveCom=="G"):
            centered=1
        
    return centered             # centered?
        
    GPIO.cleanup()
    
def inchUp(position, minAll, max1, max2, max3):
    ready=0
    driveCom="G"
    ser.write(driveCom)
    while (position==0):
        centered = center(driveCom, minAll, max1, max2, max3)          #Centering up robot
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
                else:
                    ready=ready+1
                count=count+1
                print ready
                
        if (ready>3):
            position=1  
    
    return position


def search(state, max1, max2, max3, minAll):
    
    farval= 50
    medval=30
    closeval=16
    blinkCount=0
    blinkTime=normalBlink
    
    while state == 4:
        if (GPIO.input(SButton) == 1):
            state = 5                                #return a state of 5 so manual state control can occur
       
        #blink while waiting for search    
        if(blinkCount<=blinkTime):
             GPIO.output(Status2, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(blinkTime<blinkCount<=(blinkTime*2)):
             GPIO.output(Status2, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
        
        
        if (GPIO.input(SeButton) == 1):

            time.sleep(5)                                       #Wait 5 seconds before searching 
            servoCom="Y"                #set servo to start position
            ser.write(servoCom)
            blinkTime=runBlink                                #Set blink slower
            driveCom = "G"  
            ser.write(driveCom)                               #Set start speed of robot
            while state ==4:
                if (GPIO.input(SButton) == 1):
                    driveCom="G"
                    ser.write(driveCom)
                    #print str(driveCom)
                    state = 5                                #return a state of 5 so manual state control can occur
       
       
                if(blinkCount<=blinkTime):
                    GPIO.output(Status2, GPIO.HIGH)
                    blinkCount = blinkCount+1
                elif(blinkTime<blinkCount<=(blinkTime*2)):
                    GPIO.output(Status2, GPIO.LOW)
                    blinkCount = blinkCount +1
                else:
                    blinkCount=0
                
                
                #print str(driveCom)
                
                FlameRead = readFlames(Flame1, Flame2, Flame3) 
                flame1= FlameRead['FlameRead1']
                flame2= FlameRead['FlameRead2']
                flame3= FlameRead['FlameRead3']

    
                ScaledFlame1=translate(flame1, minAll, max1, 5, 100)
                ScaledFlame2=translate(flame2, minAll, max2, 5, 100)
                ScaledFlame3=translate(flame3, minAll, max3, 5, 100)
                # print(ScaledFlame1)
                # print(ScaledFlame2)
                # print(ScaledFlame3) 

                # time.sleep(.01)

                lowestFlame = min(ScaledFlame1, ScaledFlame2, ScaledFlame3)
                if lowestFlame< closeval:
                    position=inchUp(0, minAll, max1, max2, max3)
                    if position==1:
                        state=6
                        GPIO.output(Status2, GPIO.LOW)
            #-----------------------------------------------------------------------comment out when no ultras present 
                if lowestFlame >= closeval:
                    SonarR = readSonar(Ultra4T, Ultra4E)
                    SonarL= readSonar(Ultra3T, Ultra3E)
                    SonarC = readSonar(Ultra2T, Ultra2E)
                    SonarB = readSonar(Ultra1T, Ultra1E)
                    lowest= min(SonarR, SonarL, SonarC, SonarB)
                    # if lowest < 0:
                    #     driveCom="G"
                    #     ser.write(driveCom)
                    #     while(state==4):
                    #         GPIO.output(Status1, GPIO.HIGH)
                    #         GPIO.output(Status2, GPIO.LOW)            #LED pattern for failed ultrasonic
                    #         GPIO.output(Status3, GPIO.HIGH)
                    #         GPIO.output(Status4, GPIO.LOW)
                    #         GPIO.output(Status5, GPIO.HIGH)
                            #   if (GPIO.input(SButton) == 1):
                            #       driveCom="G"
                            #       ser.write(driveCom)
                            #       state = 3                                #return a state of 3 so manual state control can occur
                    
                    if (lowest <= 25):
                        driveCom="G"
                        ser.write(driveCom)
                        thing=1
                        while thing==1:
                            GPIO.output(Status1, GPIO.HIGH)
                            GPIO.output(Status2, GPIO.LOW)            #LED pattern for thing in way
                            GPIO.output(Status3, GPIO.LOW)
                            GPIO.output(Status4, GPIO.LOW)
                            GPIO.output(Status5, GPIO.HIGH)
                            SonarR = readSonar(Ultra4T, Ultra4E)
                            SonarL= readSonar(Ultra3T, Ultra3E)
                            SonarC = readSonar(Ultra2T, Ultra2E)
                            SonarB = readSonar(Ultra1T, Ultra1E)
                            lowest= min(SonarR, SonarL, SonarC, SonarB)
                            if (lowest > 25):
                                thing=0
                                GPIO.output(Status1, GPIO.LOW)
                                GPIO.output(Status2, GPIO.LOW)            #LED pattern for thing in way
                                GPIO.output(Status3, GPIO.LOW)
                                GPIO.output(Status4, GPIO.LOW)
                                GPIO.output(Status5, GPIO.LOW)
            
            
                #------------------------------------------------------------------comment out when no ultras present
            
                if ((closeval<=lowestFlame<=farval) and (lowestFlame != ScaledFlame2)  ):        #if the flame isn't too close or too far, flame sensors should have a large difference between sides
                    newDrive="G"
                    if (newDrive !=driveCom):
                        driveCom=newDrive
                        ser.write(driveCom)
                    centered = center(driveCom, minAll, max1, max2, max3)
                    

                #print("lowest: " + str(lowestFlame))
                if lowestFlame >= farval:                               #Determine speed of robot based on perceived distance
                    newDrive="C"
                elif (lowestFlame >=medval):
                    newDrive= "B"
                elif (lowestFlame >=closeval):
                    newDrive="A"    
                elif lowestFlame <closeval:
                    newDrive="G"
                if (newDrive !=driveCom):
                    driveCom=newDrive
                    ser.write(driveCom)
                #print str(driveCom)

            
    
    return state