#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial

import time
UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

ser.open()

while(1):
    Command = raw_input("Servo position? (1/2/0/x):")
  
    if Command == '1':
        #print("Position 1")
        driveCom="D"
        ser.write(driveCom)
        driveCom="G"
        ser.write(driveCom)
        
    if Command == '2':
        driveCom="E"
        ser.write(driveCom)
        driveCom="G"
        ser.write(driveCom)
        
        
    if Command == '0':
        print("0 percent")
            
        
    
        if Command == 'x':
    
            print("Program end")
            exit()
