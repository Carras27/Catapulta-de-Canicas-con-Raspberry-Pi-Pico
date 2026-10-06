#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, I2C
import time

from pololu import IMU

# Constants for sensors
SENSITIVITY_baro = 4096 # (LSB/hPa)
SENSITIVITY_accel = 0.061 # (mg/LSB)
SENSITIVITY_gyro = 4.375  # (mdps/LSB)
SENSITIVITY_mag = 6842   # (LSB/gauss)
SENSITIVITY_temp = 8   #LSB/C
# Variable for the multi-sensor object
m_sense = None


def init():
    global m_sense
    i2c = I2C(1, scl = Pin(15), sda = Pin(14))
    m_sense = IMU(i2c)
    #m_sense.barometer_init(IMU.BAROMETER_FREQ_1HZ)
    
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_13HZ,IMU.ACCELEROMETER_SCALE_2G)
    
    m_sense.gyroscope_init(IMU.GYROSCOPE_FREQ_13HZ, IMU.GYROSCOPE_SCALE_125DPS)
    
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_0_625HZ, IMU.MAGNETOMETER_SCALE_4GAUSS)
    time.sleep(1)


def main():
    init()

    while True:
        baro_raw = m_sense.barometer_raw_data()
        baro = baro_raw / SENSITIVITY_baro
        
        acc_linear_raw = m_sense.accelerometer_raw_data()
        g_convert = 0.0098
        accx = acc_linear_raw["x"]*SENSITIVITY_accel*g_convert
        accy = acc_linear_raw["y"]*SENSITIVITY_accel*g_convert
        accz = acc_linear_raw["z"]*SENSITIVITY_accel*g_convert
        
        gyro_convert = 0.001
        gyro_raw = m_sense.gyroscope_raw_data()
        gyrox = gyro_raw["x"]/SENSITIVITY_gyro*gyro_convert 
        gyroy = gyro_raw["y"]/SENSITIVITY_gyro*gyro_convert
        gyroz = gyro_raw["z"]/SENSITIVITY_gyro*gyro_convert
        
        mag_raw = m_sense.magnetometer_raw_data()
        magx = mag_raw["x"]/SENSITIVITY_mag
        magy = mag_raw["y"]/SENSITIVITY_mag
        magz = mag_raw["z"]/SENSITIVITY_mag
        
        temp = m_sense.lsm6ds33_raw_temp() /SENSITIVITY_temp
       
        
         
        acc_linear_raw = m_sense.accelerometer_raw_data()
        mag_raw = m_sense.magnetometer_raw_data()
        g_convert = 0.0098
        calculating_avg = []


        
        magx = abs(mag_raw["x"]/SENSITIVITY_mag)
        magy = abs(mag_raw["y"]/SENSITIVITY_mag)
        magz = abs(mag_raw["z"]/SENSITIVITY_mag)
        mag_sum = magx + magy + magz
      
        print(abs(mag_sum))
        time.sleep(1)

if __name__ == "__main__":
    main()
