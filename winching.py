"""Function for winching (winching time is dependent on the ball type)."""

from machine import Pin, PWM
import time

#servo for the non metal balls
servo = PWM(Pin(20))
servo.freq(50)

#servo for the metal balls
servo_2 = PWM(Pin(19))
servo_2.freq(50)

# L298N control pins
IN1 = Pin(8, Pin.OUT)
IN2 = Pin(9, Pin.OUT)
IN3 = Pin(10, Pin.OUT)
IN4 = Pin(11, Pin.OUT)

# Full-step sequence 
FULL_STEP = [
    (1,0,1,0),
    (0,1,1,0),
    (0,1,0,1),
    (1,0,0,1)
]

direction = 1   # 1 = forward, -1 = backward
speed_ms = 10   # delay between steps in milliseconds
prev_dir = 0
prev_steps = 0



def apply_step(pattern):
    """Pattern for moving the stepper."""
    IN1.value(pattern[0])
    IN2.value(pattern[1])
    IN3.value(pattern[2])
    IN4.value(pattern[3])


def step(steps, direction, speed_ms, state):
    """Function for moving the stepper by x amount of steps either forward or backwards."""
    seq = FULL_STEP if direction == 1 else list(reversed(FULL_STEP))

    for _ in range(steps / 4):
        for pattern in seq:
            apply_step(pattern)
            time.sleep(speed_ms / 1000.0)
    # Stepper controller pins to low so the stepper doesn't pull current.
    if state == "DONT_HOLD":
        IN1.value(0)
        IN2.value(0)
        IN3.value(0)
        IN4.value(0)


def rotate_winch(ball_type, state):
    """Winching with the stepper."""
    global prev_steps
    
    if ball_type == "WHITE" or ball_type == "MARBLE":
        step(350, -1, speed_ms, state)
        prev_steps = 350
    
    elif ball_type == "BALL_ON":
        step(250, -1, speed_ms, state)
        prev_steps = 250

    elif ball_type == "METAL" or ball_type == "METAL_MAG":
        step(525, -1, speed_ms, state)
        prev_steps = 525
    return prev_steps


def rotate_winch_back(steps, state):
    """After throwing the ball the winch needs to go back to original pos"""
    step(steps, 1, speed_ms, state)
        

def servo_function_metal(input_degree):
    """Servo that holds the throwing arm in place until 
    the stepper unwinds. Time constants and angles need testing. NON METAL BALLS"""
    
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))

    servo.duty_ns(pwm_input)
    time.sleep(0.05)
    

def servo_function_non_metal(input_degree):
    """Servo that holds the throwing arm in place until 
    the stepper unwinds. Time constants and angles need testing. METAL BALLS"""

    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))

    servo_2.duty_ns(pwm_input)
    time.sleep(0.05)

"""
back = rotate_winch("MARBLE", "HOLD")
servo_function_non_metal(75)
rotate_winch_back(back, "DONT_HOLD")
servo_function_non_metal(180)
time.sleep(1)
servo_function_non_metal(0)"""

#servo_function_non_metal(0)



