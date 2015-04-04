import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

motorPWM= "P8_19"
motorA="P8_20"
motorB="P8_21"
pot = "P9_33"

GPIO.setup(motorA,GPIO.OUT)
GPIO.setup(motorB,GPIO.OUT)

ADC.setup()
PWM.start(motorPWM,0, 500)



while(1):
    
    potVal=ADC.read(pot)
    GPIO.output(motorA, GPIO.HIGH)
    GPIO.output(motorB, GPIO.LOW)
    PWM.set_duty_cycle(motorPWM, (100*potVal))
#    Command = raw_input("Servo position? (1/2/0/x):")
  
    # if Command == '1':
    #     print("Position 1")
    #     PWM.set_duty_cycle(servo, 5)
    # if Command == '2':
    #     print("Position 2")
    #     PWM.set_duty_cycle(servo, 10)
        
    # if Command == '0':
    #     print("0 percent")
    #     PWM.set_duty_cycle(servo, 0)    
        
    
    # if Command == 'x':
    
    #     print("Program end")
    #     PWM.stop("P8_13")
    #     PWM.cleanup()
    #     exit()


    

#    CDSreading = ADC.read(CDS)
#    print(str(CDSreading))
#    time.sleep(.1)
