#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.UART as UART
import serial
import time


farval = 500
medval = 200
closeval = 105
driveCom = "F"

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 9600)

RGBflame1R= "P9_16"
RGBflame1B= "P9_14"
RGBflame2R= "P9_22"
RGBflame2B= "P9_21"
RGBflame3R= "P9_31"
RGBflame3B= "P9_29"
Flame1 = "P9_40"
Flame2 = "P9_38"
Flame3 = "P9_36"
ADC.setup()
PWM.start(RGBflame1R , 0)
PWM.start(RGBflame1B , 0)
PWM.start(RGBflame2R , 0)
PWM.start(RGBflame2B , 0)
PWM.start(RGBflame3R , 0)
PWM.start(RGBflame3B , 0)

ser.open()

def flameReact(sen, RGBR, RGBB, far, med, close):
    if sen >= far:
        #PWM.set_duty_cycle(RGBR, 100)
        #PWM.set_duty_cycle(RGBB, 0)
        print("")
    elif (far >= sen >=close):
        #PWM.set_duty_cycle(RGBR, 25)
        #PWM.set_duty_cycle(RGBB, 75)
        print ("")
    elif sen <=close:
        #PWM.set_duty_cycle(RGBR, 0)
        #PWM.set_duty_cycle(RGBB, 100)
        print("closer")

while(1):
    Flame1reading = ADC.read_raw(Flame1)
    Flame2reading = ADC.read_raw(Flame2)
    Flame3reading = ADC.read_raw(Flame3)
    print(str(Flame1reading) + " " + str(Flame2reading) + " " + str(Flame3reading ) )

    time.sleep(.01)
    flameReact(Flame1reading, RGBflame1R, RGBflame1B, farval, medval, closeval)
    flameReact(Flame2reading, RGBflame2R, RGBflame2B, farval, medval, closeval)
    flameReact(Flame1reading, RGBflame3R, RGBflame3B, farval, medval, closeval)
    lowest = min(Flame1reading, Flame2reading, Flame3reading)
    print("lowest: " + str(lowest))
    if lowest >= farval:
        driveCom="B"
    elif (farval >= lowest >=closeval):
        driveCom="A"
    elif lowest <=closeval:
        driveCom="F"
    ser.write(driveCom)
    

    if KeyboardInterrupt:
        GPIO.cleanup()
        PWM.cleanup()
