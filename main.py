import time
from ball_from_buffer import turn_wheel
from weight_imu import weighing_function, weighing_function_empty
from WnC_base_rotation import rotate_baseplate
from winching import servo_function_non_metal, servo_function_metal, rotate_winch, rotate_winch_back
from lcd_display import display, display_clear

    
def main():
    """Main loop that controls the robots movement pattern."""

    while True:
        
        #Pull the arm back so it kills all the vibration
        rotate_winch("BALL_ON", "DONT_HOLD")
        rotate_winch_back(250, "DONT_HOLD")
        
        
        #pull the stick down so the ball can roll in
        empty_imu_weight = weighing_function_empty()
        time.sleep(1)
        rotate_winch_steps = rotate_winch("BALL_ON", "DONT_HOLD") 
        time.sleep(2)

        #turn the wheel so it picks up a ball
        turn_wheel(75000)
        time.sleep(4)

        #after the ball is in let the stick go back up
        rotate_winch_back(rotate_winch_steps, "DONT_HOLD")
        time.sleep(5)

        #weigh the ball
        ball_type = weighing_function(empty_imu_weight[0], empty_imu_weight[1])
        print(ball_type)
        display(f"Ball type:\n{ball_type}")

        #rotate the baseplate to its corresponding outlet
        
        if ball_type != "METAL_MAG":
            rotate_baseplate(ball_type, "FORWARD")
            time.sleep(2)

        #rotate the winch based on the ball type
        prev_steps = rotate_winch(ball_type, "HOLD")
        time.sleep(1)

        #turn the servo based on the ball type so the stick stays in the lowered position
        if ball_type == "METAL" or ball_type == "METAL_MAG":
            servo_function_metal(80)
            time.sleep(1)
        else:
            servo_function_non_metal(75)
            time.sleep(1)

        #let the winch unwind
        rotate_winch_back(prev_steps, "DONT_HOLD")
        time.sleep(1)

        #pull the servos arm back so it releases the stick for the metal balls
        #or push the stick down for non-metal balls.
        if ball_type == "METAL" or ball_type == "METAL_MAG":
            servo_function_metal(0)
        else:
            servo_function_non_metal(180)
            time.sleep(1)
            servo_function_non_metal(0)
    
    
        if ball_type != "METAL_MAG":
            rotate_baseplate(ball_type, "BACK")
            time.sleep(1)
        
        display_clear()


if __name__ == "__main__":
    main()
