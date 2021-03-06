#sensor_calc.py
import time
import numpy as np
import adafruit_bno055
import time
import os
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_bno055.BNO055_I2C(i2c)
sensor2 = adafruit_bno055.BNO055_I2C(i2c)


#Activity 1: RPY based on accelerometer and magnetometer
def roll_am(accelX,accelY,accelZ):
    roll = np.arctan2(accelY, np.sqrt(accelX**2 + accelZ**2))
    return np.rad2deg(roll) 

def pitch_am(accelX,accelY,accelZ):
    pitch = np.arctan2(accelX, np.sqrt(accelY**2 + accelZ**2))
    return np.rad2deg(pitch)

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    roll = np.deg2rad( roll_am(accelX,accelY,accelZ))
    pitch = np.deg2rad( pitch_am(accelX,accelY,accelZ))

    mag_x = (magX * np.cos(pitch) +
             magY * np.sin(roll) * np.sin(pitch) + 
             magZ * np.cos(roll) * np.cos(roll))

    mag_y = magY * np.cos(roll) - magZ * np.sin(roll)
    return np.rad2deg ( np.arctan2 (-mag_y, mag_x) )

#Activity 2: RPY based on gyroscope
def roll_gy(prev_angle, delT, gyro):
    roll = prev_angle - gyro*delT
    return roll
def pitch_gy(prev_angle, delT, gyro):
    pitch = prev_angle - gyro*delT
    return pitch
def yaw_gy(prev_angle, delT, gyro):
    yaw = prev_angle - gyro*delT
    return yaw

def set_initial(mag_offset = [0,0,0]):
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = sensor1.acceleration #m/s^2
    magX, magY, magZ = sensor1.magnetic #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    print("Initial angle set.")
    print (roll,pitch, yaw)
    return [roll,pitch,yaw]

def calibrate_mag(dataRate = 10, collectionPeriod = 1):
    #dataRate in Hz
    #collectionPeriod in sec

    nPoints = dataRate * collectionPeriod
    waitTime = 1/dataRate

    print("Preparing to calibrate magnetometer. Please wave around.")
    time.sleep(3)
    print("Calibrating...")

    mag = []

    for i in range(nPoints):
        mag.append(sensor1.magnetic)
        time.sleep(waitTime)
    mag = np.transpose(np.array(mag))
    minAll = np.min(mag, axis=1)
    maxAll = np.max(mag, axis=1)
    calib = (minAll + maxAll) / 2
    
    print("Calibration complete.")

    return calib

def calibrate_gyro(dataRate = 10, collectionPeriod = 1):
    nPoints = dataRate * collectionPeriod
    waitTime = 1/dataRate
    print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    time.sleep(3)
    print("Calibrating...")
    
    gyro = []

    for i in range(nPoints):
        gyro.append(sensor2.gyro)  #rad/s
        time.sleep(waitTime)
    gyro = np.transpose(np.array(gyro))
    minAll = np.min(gyro, axis=1)
    maxAll = np.max(gyro, axis=1)
    gyro_calib = (minAll + maxAll) / 2
    print("Calibration complete.")
    return gyro_calib
