"""Using the IMU to weigh the balls."""

from machine import Pin, I2C
import time
from pololu import IMU


# Constant for the sensor
SENSITIVITY_accel = 0.061 # (mg/LSB)
SENSITIVITY_mag = 6842   # (LSB/gauss)
m_sense = None


def init():
    """Getting accelerometer data"""
    global m_sense
    i2c = I2C(1, scl = Pin(15), sda = Pin(14))
    
    m_sense = IMU(i2c)  
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_13HZ,IMU.ACCELEROMETER_SCALE_2G)
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_0_625HZ, IMU.MAGNETOMETER_SCALE_4GAUSS)
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_0_625HZ, IMU.MAGNETOMETER_SCALE_4GAUSS)
    
    time.sleep(1)


def weighing_function(empty, prev_mag):
    init()
    """Looking at the accelerometer data on the x axis."""  
    acc_linear_raw = m_sense.accelerometer_raw_data()
    mag_raw = m_sense.magnetometer_raw_data()
    g_convert = 0.0098
    calculating_avg = []


    for _ in range(50):
        accx = acc_linear_raw["x"]*SENSITIVITY_accel*g_convert
        calculating_avg.append(accx)
    
    magx = abs(mag_raw["x"]/SENSITIVITY_mag)
    magy = abs(mag_raw["y"]/SENSITIVITY_mag)
    magz = abs(mag_raw["z"]/SENSITIVITY_mag)
    mag_sum = magx + magy + magz
    accx = sum(calculating_avg) / len(calculating_avg)
  
    print(f"With ball ACC X: {accx:.2f} m/s2")
    print(accx - empty)
    print(abs(prev_mag - mag_sum))
    # Thresholds are not set in stone.
    if accx - empty == 0:
        return "Empty"
    elif accx - empty > 0.05 and accx - empty <= 0.33:
        return "WHITE"
    elif accx - empty > 0.33 and accx - empty <= 0.6:
        return "MARBLE"
    elif accx  - empty > 0.6 and abs(prev_mag - mag_sum) > 0.5:
        return "METAL_MAG"
    else:
        return "METAL"
    


def weighing_function_empty():
    init()
    """Looking at the accelerometer data on the x axis."""  
    acc_linear_raw = m_sense.accelerometer_raw_data()
    mag_raw = m_sense.magnetometer_raw_data()
    g_convert = 0.0098
    calculating_avg = []


    for _ in range(50):
        accx = acc_linear_raw["x"]*SENSITIVITY_accel*g_convert
        calculating_avg.append(accx)
        
    magx = abs(mag_raw["x"]/SENSITIVITY_mag)
    magy = abs(mag_raw["y"]/SENSITIVITY_mag)
    magz = abs(mag_raw["z"]/SENSITIVITY_mag)
    mag_sum = magx + magy + magz
    accx = sum(calculating_avg) / len(calculating_avg)
    print(f"EMPTY ACC X: {accx:.2f} m/s2")
    print(magy)
    return [accx, mag_sum]
    

             