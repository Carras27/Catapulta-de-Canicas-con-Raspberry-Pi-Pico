"""Functions for getting the ball onto the throwing arm."""
from machine import Pin,PWM, ADC
import time


# Center is 1.5ms or 1500000ns
center = 1500000
servo = PWM(Pin(21))
servo.freq(50)
servo.duty_ns(center)
time.sleep(0.2)

#button  = Pin(26, Pin.IN, Pin.PULL_UP)
hall = ADC(Pin(26,Pin.IN))



"""
def turn_wheel(speed):
    Servo that spins the wheel that picks up the balls.   
    servo.duty_ns(center + speed)
    time.sleep(0.7)
    while True:
        if button.value() == 0:
            servo.duty_ns(center)
            break
    
    time.sleep(0.2) 
    servo.deinit()
    pin = Pin(0, Pin.OUT)
    pin.low()"""

def turn_wheel(speed):
    
    servo.duty_ns(center + speed)
    time.sleep(0.7)
    default_reading = hall.read_u16()
    while True:
        test = hall.read_u16()
        if test / default_reading < 0.95:
            servo.duty_ns(center)
            break
    
    time.sleep(0.2) 
    servo.deinit()
    pin = Pin(0, Pin.OUT)
    pin.low()

#turn_wheel(75000)

    



