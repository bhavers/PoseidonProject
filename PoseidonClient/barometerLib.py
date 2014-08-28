'''
Created on 26.07.2014

@author: hymas
'''

# Re-written from: https://github.com/Seeed-Studio/Grove_Barometer_HP20x

# Datasheet: http://www.seeedstudio.com/wiki/images/d/d8/HP206C_Datasheet.pdf

import smbus
import time
import RPi.GPIO as GPIO
import sys


rev = GPIO.RPI_REVISION
if rev == 2:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

HP20X_I2C_DEV_ID        = 0x76 # Barometer device address
HP20X_SOFT_RST          = 0x06 # Soft reset the device
REG_PARA                = 0X0F # Status register

HP20X_RD_REG_MODE       = 0x80
HP20X_WR_CONVERT_CMD    = 0x40

HP20X_READ_P            = 0x30
HP20X_READ_A            = 0x31
HP20X_READ_T            = 0x32

HP20X_CONVERT_OSR1024   = 2<<2

OK_HP20X_DEV            = 0X80

OSR_CFG                 = HP20X_CONVERT_OSR1024
OSR_ConvertTime         = 25.0



def isAvailable():
# Check if Compensation is enabled
# 0x80 == Read Register ; 0xF == Register Address
# 0x0F | 0x80 = 0x8F
    bus.write_byte(HP20X_I2C_DEV_ID, REG_PARA|HP20X_RD_REG_MODE)
# Retrieve the actual value from sensor
# 0x76
    ret = bus.read_byte(HP20X_I2C_DEV_ID)
# Check if disabled/enabled ( 0x80 is default == On )
# 0X80
    if ret == OK_HP20X_DEV:
        print "reset ok"
        return True
    else:
        print "reset failed"
        return False

def readSensor(sensor):
# Set analog to digital conversion rate
# 0x40 == ADC cmd ; 2<<2 == DSR 1024 ; 00 == pressure && temp channel
# 0x40 | 2<<2 = 0x48
    bus.write_byte(HP20X_I2C_DEV_ID, HP20X_WR_CONVERT_CMD|OSR_CFG)
    time.sleep(OSR_ConvertTime/1000.0)
# Send cmd to read from sensor X
# 0x30 || 0x31 || 0x32
    bus.write_byte(HP20X_I2C_DEV_ID, sensor)
# Read data from bus
    data=bus.read_i2c_block_data(HP20X_I2C_DEV_ID,0)
    value = data[0]<<16 | data[1]<<8 | data[2]
    return value

# Send Soft reset
# 0x06
bus.write_byte(HP20X_I2C_DEV_ID, HP20X_SOFT_RST)
time.sleep(0.1)

if isAvailable():
    print "Barometer Available"
else:
    print "Barometer Not Available"
    sys.exit()





