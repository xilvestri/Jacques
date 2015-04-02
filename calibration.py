#!/usr/bin/python

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import numpy as np

#Define Flame sensors
Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
CButton= "P8_18"
SButton= "P8_10"
Status1="P8_11"
thermistor = "P9_39"
ADC.setup()
GPIO.setup(CButton, GPIO.IN)
GPIO.setup(Status1, GPIO.OUT)


def calibration(state):
    
    #Create lists for sensor readings not at flame, and at flame. Lists created for each sensor
    noFlame1 = []
    noFlame2 = []
    noFlame3 = []
    yesFlame1 = []
    yesFlame2 = []
    yesFlame3 = []
    full=[1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0, 1799.0,]
    
    #Cflag set for what stage of calibration the button collects for
    Cflag=0
    #blinkcount controls Status light blink
    blinkCount=0
    
    #State goes on while under calibration
    while (state== 2):
        
        #Blinks LED when waiting for calibration command
        if(blinkCount<=1400):
             GPIO.output(Status1, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(1400<blinkCount<=2800):
             GPIO.output(Status1, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
            
        
        if (GPIO.input(SButton) == 1):
            state = 3                                #return a state of 3 so manual state control can occur
        
        #Collect flame sensor and thermistor values when not near flame
        if (GPIO.input(CButton) == 1 and Cflag == 0):
            #blink status LED quickly
            for x in range(0,50):
                time.sleep(.03)
                if (x<=3 or 6<x<=9 or 12<x<=15 or 18<x<=21 or 24<x<=27 or 30<x<=33 or 36<x<=39 or 42<x<=45 or 48<x<=50):
                    GPIO.output(Status1, GPIO.HIGH)
                else:
                    GPIO.output(Status1, GPIO.LOW)
                
                #collect values of sensor
                Flame1reading = ADC.read_raw(Flame1)
                Flame2reading = ADC.read_raw(Flame2)
                Flame3reading = ADC.read_raw(Flame3)
                
                noFlame1 = noFlame1 + [Flame1reading]
                noFlame2 = noFlame2 + [Flame2reading]
                noFlame3 = noFlame3 + [Flame3reading]

            
            #eliminate outliers if found. If all values eliminated, robot is reading all ful distance signals and does not see the flame.
            noFlame1=[e for e in noFlame1 if (np.median(noFlame1)-2*np.std(noFlame1) < e <np.median(noFlame1) +2 * np.std(noFlame1))]
            if len(noFlame1)==0:
                noFlame1=full
            noFlame2=[e for e in noFlame2 if (np.median(noFlame2)-2*np.std(noFlame2) < e <np.median(noFlame2) +2 * np.std(noFlame2))]
            if len(noFlame2)==0:
                noFlame2=full
            noFlame3=[e for e in noFlame3 if (np.median(noFlame3)-2*np.std(noFlame3) < e <np.median(noFlame3) +2 * np.std(noFlame3))]
            if len(noFlame3)==0:
                noFlame3=full
            
            #takes average of values and stores for future use.
            noAverage1 = np.mean(noFlame1)
            noAverage2 = np.mean(noFlame2)
            noAverage3 = np.mean(noFlame3)
            
            #reads a thermistor value
            nothermistor=ADC.read_raw(thermistor)

            #print "no"
            #print noAverage1
            #print noAverage2
            #print noAverage3

            #first collection complete. Flag for second collection
            Cflag=1
            
        #once no flame values collected, repeat for at flame collection
        if (GPIO.input(CButton) == 1 and Cflag == 1):    
            for x in range(0,50):
                time.sleep(.03)
                if (x<=3 or 6<x<=9 or 12<x<=15 or 18<x<=21 or 24<x<=27 or 30<x<=33 or 36<x<=39 or 42<x<=45 or 48<x<=50):
                    GPIO.output(Status1, GPIO.HIGH)
                else:
                    GPIO.output(Status1, GPIO.LOW)
                

                Flame1reading = ADC.read_raw(Flame1)
                Flame2reading = ADC.read_raw(Flame2)
                Flame3reading = ADC.read_raw(Flame3)
                yesFlame1 = yesFlame1 + [Flame1reading]
                yesFlame2 = yesFlame2 + [Flame2reading]
                yesFlame3 = yesFlame3 + [Flame3reading]

            yesFlame1=[e for e in yesFlame1 if (np.median(yesFlame1)-2*np.std(yesFlame1) < e <np.median(yesFlame1) +2 * np.std(yesFlame1))]
            if len(yesFlame1)==0:
                yesFlame1=full
            yesFlame2=[e for e in yesFlame2 if (np.median(yesFlame2)-2*np.std(yesFlame2) < e <np.median(yesFlame2) +2 * np.std(yesFlame2))]
            if len(yesFlame2)==0:
                yesFlame2=full
            yesFlame3=[e for e in yesFlame3 if (np.median(yesFlame3)-2*np.std(yesFlame3) < e <np.median(yesFlame3) +2 * np.std(yesFlame3))]
            if len(yesFlame3)==0:
                yesFlame3=full
            
            yesAverage1 = np.mean(yesFlame1)
            yesAverage2 = np.mean(yesFlame2)
            yesAverage3 = np.mean(yesFlame3)

            
            lowestAverage=min(yesAverage1,yesAverage2,yesAverage3)
            

            #print "yes"
            #print yesAverage1
            #print yesAverage2
            #print yesAverage3
            
            
            
            #Check for validity of values. Checks for large gap between no flame and at flame readings. 
            #Also prompts for redo when too many outliers found
            if noAverage1 < lowestAverage *2 or noAverage2 < lowestAverage *2 or noAverage3 < lowestAverage*2 or len(yesFlame1)<40 or len(yesFlame2)<40 or len(yesFlame3)<40 or len(noFlame1)<40 or len(noFlame2)<40 or len(noFlame3)<40:
                Cflag = 0 
                state = 2
                noFlame1 = []
                noFlame2 = []
                noFlame3 = []
                yesFlame1 = []
                yesFlame2 = []
                yesFlame3 = []
                #print"problem"
 
            
            else:
                state=4 #Program goes directly to search phase
                Cflag=2
                GPIO.output(Status1, GPIO.LOW)

            
    return {'state':state, 'maxVal1': noAverage1, 'maxVal2' : noAverage2, 'maxVal3': noAverage3, 'minVal': lowestAverage, 'minTherm': nothermistor}
