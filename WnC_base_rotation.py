"""Functions for rotating the baseplate a certain amount and getting back to the original position."""
from machine import Pin, ADC
import time

# L298N control pins
IN1 = Pin(0, Pin.OUT)
IN2 = Pin(1, Pin.OUT)
IN3 = Pin(2, Pin.OUT)
IN4 = Pin(3, Pin.OUT)

# Full-step sequence 
FULL_STEP = [
    (1,0,1,0),
    (0,1,1,0),
    (0,1,0,1),
    (1,0,0,1)
]

direction = 1   # 1 = forward, -1 = backward
speed_ms = 13   # delay between steps in milliseconds
new_dir = 0
prev_steps = 0

#light sensor
light_sensor = ADC(Pin(27, Pin.IN))
#led for sensor
led = Pin(13, Pin.OUT)


led.value(0)

def apply_step(pattern):
    """Pattern for moving the stepper."""
    IN1.value(pattern[0])
    IN2.value(pattern[1])
    IN3.value(pattern[2])
    IN4.value(pattern[3])


def step(direction, speed_ms):
    """Function for moving the stepper by x amount of steps either forward or backwards."""
    seq = FULL_STEP if direction == 1 else list(reversed(FULL_STEP))

    for i in range(1):
        for pattern in seq:
            apply_step(pattern)
            time.sleep(speed_ms / 1000.0)

    # Stepper controller pins to low so the stepper doesn't pull current.
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


def rotate_baseplate(ball_type, direction):
    """Rotates the baseplate a certain amount based on the type of ball."""
    state = "NOT_LINE"
    prev_state = "ON_LINE"
    line_count = 0
    needed_line_count = 0
    led.value(1)
    time.sleep(1)
    default_all = []
    for i in range(50):
        
        default_data = light_sensor.read_u16()
        default_all.append(default_data)
    
    default_data = sum(default_all) / 50
    
    if ball_type == "WHITE":
        needed_line_count = 2
        if direction == "FORWARD":
            direction = 1
        else:
            direction = -1

    elif ball_type == "MARBLE":
        needed_line_count = 1
        if direction == "FORWARD":
            direction = -1
        else:
            direction = 1
        
    elif ball_type == "METAL":
        needed_line_count = 1
        if direction == "FORWARD":
            direction = 1
        else:
            direction = -1
        
    while True:
        
        data_all = []
        for i in range(50):
            data = light_sensor.read_u16()
            data_all.append(data)
            
        data = sum(data_all) / 50   
        step(direction, speed_ms)
        if data == 0:
            continue
        else:
            
            if default_data / data > 0.7 and default_data / data < 0.75 and line_count < needed_line_count:
                continue
            
            elif default_data / data < 0.7 and line_count < needed_line_count:
                state = "NOT_LINE"
                if prev_state == "ON_LINE":
                    prev_state = "NOT_LINE"            
        
            elif default_data / data > 0.75 and line_count < needed_line_count:
                state = "ON_LINE"
                
                if prev_state == "NOT_LINE":
                    prev_state = "ON_LINE"
                    line_count +=1
            
            else:
                break
    
    led.value(0)

"""
rotate_baseplate("WHITE", "FORWARD")
time.sleep(2)
rotate_baseplate("WHITE", "BACK")"""
