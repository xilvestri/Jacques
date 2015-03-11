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
    
    #Cflag set for what stage of calibration the button collects for
    Cflag=0
    #blinkcount controls Status light blink
    blinkCount=0
    
    #State goes on while under calibration
    while (state== 2):
        
        #Blinks LED when waiting for calibration command
        if(blinkCount<=700):
             GPIO.output(Status1, GPIO.HIGH)
             blinkCount = blinkCount+1
        elif(700<blinkCount<=1400):
             GPIO.output(Status1, GPIO.LOW)
             blinkCount = blinkCount +1
        else:
            blinkCount=0
            
        
        if (GPIO.input(SButton) == 1):
            state = 3                                #return a state of 3 so manual state control can occur
        
        #Collect flame sensor values when not near flame
        if (GPIO.input(CButton) == 1 and Cflag == 0):
            #blink status LED quickly
            for x in range(0,50):
                if (x<=5 or 10<x<=15 or 20<x<=25 or 30<x<=35 or 40<x<=45):
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
            
            #eliminate outliers if found
            noFlame1=[e for e in noFlame1 if (np.mean(noFlame1)-2*np.std(noFlame1) < e <np.mean(noFlame1) +2 * np.std(noFlame1))]
            noFlame2=[e for e in noFlame2 if (np.mean(noFlame2)-2*np.std(noFlame2) < e <np.mean(noFlame2) +2 * np.std(noFlame2))]
            noFlame3=[e for e in noFlame3 if (np.mean(noFlame3)-2*np.std(noFlame3) < e <np.mean(noFlame3) +2 * np.std(noFlame3))]
            
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
                if (x<=5 or 10<x<=15 or 20<x<=25 or 30<x<=35 or 40<x<=45):
                    GPIO.output(Status1, GPIO.HIGH)
                else:
                    GPIO.output(Status1, GPIO.LOW)
                

                Flame1reading = ADC.read_raw(Flame1)
                Flame2reading = ADC.read_raw(Flame2)
                Flame3reading = ADC.read_raw(Flame3)
                yesFlame1 = yesFlame1 + [Flame1reading]
                yesFlame2 = yesFlame2 + [Flame2reading]
                yesFlame3 = yesFlame3 + [Flame3reading]

            yesFlame1=[e for e in yesFlame1 if (np.mean(yesFlame1)-2*np.std(yesFlame1) < e <np.mean(yesFlame1) +2 * np.std(yesFlame1))]
            yesFlame2=[e for e in yesFlame2 if (np.mean(yesFlame2)-2*np.std(yesFlame2) < e <np.mean(yesFlame2) +2 * np.std(yesFlame2))]
            yesFlame3=[e for e in yesFlame3 if (np.mean(yesFlame3)-2*np.std(yesFlame3) < e <np.mean(yesFlame3) +2 * np.std(yesFlame3))]
            
            yesAverage1 = np.mean(yesFlame1)
            yesAverage2 = np.mean(yesFlame2)
            yesAverage3 = np.mean(yesFlame3)
            
        
            yesthermistor=ADC.read_raw(thermistor)
            #print "yes"
            #print yesAverage1
            #print yesAverage2
            #print yesAverage3
            
            state=4          #Program goes directly to search phase
            
            #Check for validity of values. Checks for large gap between no flame and at flame readings. 
            #Also prompts for redo when too many outliers found
            #if noAverage1 > yesAverage1 *2 and noAverage2 > yesAverage2 and noAverage3 > yesAverage3 and len(yesFlame1)>40 and len(yesFlame2)>40 and len(yesFlame3)>40 and len(noFlame1)>40 and len(noFlame2)>40 and len(noFlame3)>40:
                #Cflag = 0 
                #state = 2
            
            Cflag=2

            
    return {'state':state, 'maxVal1': noAverage1, 'maxVal2':noAverage2,'maxVal3': noAverage3,'minVal1': yesAverage1,'minVal2': yesAverage2,'minVal3': yesAverage3, 'maxTherm':yesthermistor, 'minTherm': nothermistor}
