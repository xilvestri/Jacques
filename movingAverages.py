#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import numpy as np

sensor1 = 'P9_40'
sensor2 ='P9_38'
sensor3 ='P9_36'

ADC.setup()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
    
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

while(1):
    FlameRead = readFlames(sensor1, sensor2, sensor3) 
    flame1= FlameRead['FlameRead1']
    flame2= FlameRead['FlameRead2']
    flame3= FlameRead['FlameRead3']

    
    ScaledFlame1=translate(flame1, 200, 1799, 5, 100)
    ScaledFlame2=translate(flame2, 200, 1799, 5, 100)
    ScaledFlame3=translate(flame3, 200, 1799, 5, 100)

    print ScaledFlame1
    print ScaledFlame2
    print ScaledFlame3
    print " "
