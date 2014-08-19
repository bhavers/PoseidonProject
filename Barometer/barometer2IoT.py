'''
Created on 26.07.2014

@author: hymas
'''

# Re-written from: https://github.com/Seeed-Studio/Grove_Barometer_HP20x

import smbus
import time
import RPi.GPIO as GPIO
import sys
import mosquitto


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

OSR_CFG                 = HP20X_CONVERT_OSR1024;
OSR_ConvertTime         = 25.0; 


def isAvailable():
    bus.write_byte(HP20X_I2C_DEV_ID, REG_PARA|HP20X_RD_REG_MODE)
    ret = bus.read_byte(HP20X_I2C_DEV_ID)     

    if ret == OK_HP20X_DEV:
        print "reset ok"
        return True
    else:
        print "reset failed"
        return False

def readSensor(sensor):
      
    bus.write_byte(HP20X_I2C_DEV_ID, HP20X_WR_CONVERT_CMD|OSR_CFG)
    time.sleep(OSR_ConvertTime/1000.0)
    bus.write_byte(HP20X_I2C_DEV_ID, sensor)
    data=bus.read_i2c_block_data(HP20X_I2C_DEV_ID,0) 
    value = data[0]<<16 | data[1]<<8 | data[2]
    return value
    

bus.write_byte(HP20X_I2C_DEV_ID, HP20X_SOFT_RST)
time.sleep(0.1)

if isAvailable():
    print "Barometer Available"
else:
    print "Barometer Not Available"
    sys.exit()    

#####################################################
#
# IoT stuff
#
#####################################################

def IoT_on_message(mosq, obj, msg):

    print "IoT msg: " + str(msg.payload)        
    return    
    
def IoT_on_publish(mosq, obj, mid):
    
    #print("IoT publish mid: "+str(mid))
    return

def IoT_on_subscribe(mosq, obj, mid, granted_qos):
    
    print("IoT Subscribed OK")
    return

def IoT_on_connect(mosq, obj, rc):
    
    print("IoT connect rc: "+str(rc))
    return

def IoT_on_disconnect(mosq, obj,rc):
    print("IoT disconnect rc: " + str(rc))

##########################

tenantId = "quickstart"
deviceId = "b827ebfc9087"

clientId = "d:quickstart:piairbot:" + deviceId

print("clientId: " + clientId)

IoTc = mosquitto.Mosquitto(clientId)
IoTc.on_message = IoT_on_message
IoTc.on_connect = IoT_on_connect
IoTc.on_publish = IoT_on_publish
IoTc.on_subscribe = IoT_on_subscribe
IoTc.on_disconnect = IoT_on_disconnect

IoTc.connect("messaging.quickstart.internetofthings.ibmcloud.com", 1883, 60)

IoTc.loop_start()
IoTc._sock.setblocking(1)

msgType = "Poseidon"

topic = "iot-2/evt/status/fmt/json"

print ("topic: " + topic)

while (isAvailable()):
    temp = readSensor(HP20X_READ_T) / 100.0
    print "Temperature: " + str(temp)
    baro = readSensor(HP20X_READ_P) / 100.0
    print "Barometer: " + str(baro)
    alti = readSensor(HP20X_READ_A) / 100.0
    print "Altitude: " + str(alti)
    
    msg = "{\"d\":{\"myName\": \"Poseidon\",\"Temperatire\":" + str(temp) + ",\"Barometer\":" + str(baro) + ",\"Altitude\":" + str(alti) + "}}"
    
    IoTc.publish(topic, msg, 0)
    print ("sent: " + msg)
    
    time.sleep(5);
    



    
    
    
    


