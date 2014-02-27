#!/usr/bin/python
# encoding: utf-8
"""
Accelerometer.py

Created by Alexander Rössler on 2014-02-26.
"""

import argparse
import sys
import os
import time
#from datetime import datetime, date
from libraries.Accelerometer.Adafruit_LSM303DLHC import LSM303DLHC

import hal

parser = argparse.ArgumentParser(description='HAL component to read LSM303 Accelerometer values')
parser.add_argument('-n','--name', help='HAL component name',required=True)
parser.add_argument('-b','--bus_id', help='I2C bus id', default=1)
parser.add_argument('-i','--interval', help='I2C update interval', default=0.25)
args = parser.parse_args()

update_interval = float(args.interval)

lsm = LSM303DLHC(0x19, 0x1E, False, int(args.bus_id))
lsm.setTempEnabled(True)

h = hal.component(args.name)
h.newpin("angle", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()

while(1):
    time.sleep(update_interval)
    #accel = lsm.readAccelerationsG()
    #mag = lsm.readMagneticsGauss()
    #temp = lsm.readTemperatureCelsius()
    heading = lsm.readMagneticHeading()

    #print "Timestamp: %s" % datetime.now().isoformat() #strftime('%Y-%m-%dT%H:%M:%S(%Z)')
    #print "Accel X: %6.3f G,     Y: %6.3f G,     Z: %6.3f G" % (accel.x, accel.y, accel.z)
    #print "Mag   X: %6.3f gauss, Y: %6.3f gauss, Z: %6.3f gauss" % (mag.x, mag.y, mag.z)
    #print "Temp:    %6.3f C" % (temp)
    #print "Heading: %6.3f" % (heading)
    h['angle']=heading
