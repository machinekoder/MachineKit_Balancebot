#!/usr/bin/python
# encoding: utf-8
"""
Accelerometer.py

Created by Alexander Rössler on 2014-02-26.
"""
from libraries.Gyrometer.L3GD20 import L3GD20
from libraries.Accelerometer.Adafruit_LSM303DLHC import LSM303DLHC

import argparse
import time
import math

import hal

parser = argparse.ArgumentParser(description='HAL component to read LSM303 Accelerometer values')
parser.add_argument('-n', '--name', help='HAL component name', required=True)
parser.add_argument('-b', '--bus_id', help='I2C bus id', default=1)
parser.add_argument('-i', '--interval', help='I2C update interval', default=0.25)
args = parser.parse_args()

update_interval = float(args.interval)

# Communication object
gyro = L3GD20(busId=int(args.bus_id),
              slaveAddr=0x6B,
              ifLog=False,
              ifWriteBlock=False)
accel = LSM303DLHC(address_accel=0x19,
                   address_mag=0x1E,
                   debug=False,
                   busId=int(args.bus_id))

# Preconfiguration
gyro.Set_PowerMode("Normal")
gyro.Set_FullScale_Value("250dps")
gyro.Set_AxisX_Enabled(True)
gyro.Set_AxisY_Enabled(False)
gyro.Set_AxisZ_Enabled(False)

accel.setTempEnabled(True)
accelXzero = 0.0
accelZzero = 0.0

# Print current configuration
gyro.Init()
gyro.CalibrateX()

# Initialize HAL
h = hal.component(args.name)
h.newpin("angle", hal.HAL_FLOAT, hal.HAL_OUT)
h.newpin("rate", hal.HAL_FLOAT, hal.HAL_OUT)
h.newpin("dt", hal.HAL_FLOAT, hal.HAL_OUT)
h.newpin("request", hal.HAL_BIT, hal.HAL_IN)
h.newpin("acknowledge", hal.HAL_BIT, hal.HAL_OUT)
h.ready()

h['angle'] = 0.0
h['rate'] = 0.0
h['dt'] = 0.0
h['acknowledge'] = 0

oldTimestamp = time.time()

while(1):
    time.sleep(update_interval)

    if ((h['request'] == 1) and (h['acknowledge'] == 0)):
        gyroRate = gyro.Get_CalOutX_Value()
        accelXyz = accel.readAccelerationsG()
        newTimestamp = time.time()  # NOTE: take timestamp before or after???

        accAngle = math.degrees(math.atan2(accelXyz.x - accelXzero,
                                           accelXyz.z - accelZzero))
        h['angle'] = accAngle
        h['rate'] = gyroRate
        h['dt'] = newTimestamp - oldTimestamp
        oldTimestamp = newTimestamp
        h['acknowledge'] = 1
    elif ((h['request'] == 0) and (h['acknowledge'] == 1)):
        h['acknowledge'] = 0
