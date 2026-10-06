import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

#size of the display
lcd_columns = 16 
lcd_rows = 2     

#needed pins to connect the display
scl_pin = board.GP17
sda_pin = board.GP16
i2c = busio.I2C(scl_pin, sda_pin)

#Initialize the LCD
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)


def display(ball_type):
    """Little func for displaying info on screen"""
    lcd.clear()
    lcd.message = ball_type
    
def display_clear():
    lcd.clear()
