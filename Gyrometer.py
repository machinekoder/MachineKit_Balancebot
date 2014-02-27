#!/usr/bin/python

from libraries.Gyrometer.L3GD20 import L3GD20
from libraries.Accelerometer.Adafruit_LSM303DLHC import LSM303DLHC

import time
import math

# Communication object
s = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)

lsm = LSM303DLHC(0x19, 0x1E, False, 1)
lsm.setTempEnabled(False)

# Preconfiguration
s.Set_PowerMode("Normal")
s.Set_FullScale_Value("250dps")
s.Set_AxisX_Enabled(True)
s.Set_AxisY_Enabled(False)
s.Set_AxisZ_Enabled(False)

# Print current configuration
s.Init()
s.CalibrateX()

# Calculate angle
dt = 0.02
x = 0
y = 0
z = 0
while 1==1:
	time.sleep(dt)
	gyroRate = s.Get_CalOutX_Value()
	#dxyz = s.Get_CalOut_Value()
	#x += dxyz[0]*dt;
	#y += dxyz[1]*dt;
	#z += dxyz[2]*dt;
	
	#print("{:7.2f} {:7.2f} {:7.2f}".format(x)) #.format(dxyz[0], dxyz[1], dxyz[2]))
	#print("{:7.2f}".format(x))
        xyz = lsm.readAccelerationsG()
	timestamp = time.time()
	accAngle = math.degrees(math.atan2(xyz.x, xyz.z))
	#heading = lsm.readMagneticHeading()
	print("{:7.2f} {:7.2f} {:7.3f}".format(accAngle, gyroRate, timestamp))
	#print("{:7.2f} {:7.2f} {:7.2f}".format(xyz.x, xyz.y, xyz.z))
