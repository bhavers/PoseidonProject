'''
Created on 26.07.2014

@author: hymas
'''

# Re-written from: https://github.com/Seeed-Studio/Grove_Barometer_HP20x

import smbus
import time
import RPi.GPIO as GPIO
import sys
import struct
import mosquitto

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
deviceId = "b827eb79c763"
clientId = "d:quickstart:piairbot:" + deviceId

print "deviceId: " + deviceId

IoTc = mosquitto.Mosquitto(clientId)
IoTc.on_message = IoT_on_message
IoTc.on_connect = IoT_on_connect
IoTc.on_publish = IoT_on_publish
IoTc.on_subscribe = IoT_on_subscribe
IoTc.on_disconnect = IoT_on_disconnect

IoTc.connect("messaging.quickstart.internetofthings.ibmcloud.com", 1883, 60)
#IoTc.connect("realtime.ngi.ibm.com", 1883, 60)

IoTc.loop_start()
IoTc._sock.setblocking(1)
topic = "iot-2/evt/status/fmt/json"
#print "Topic: " + topic

dustRead_cmd=[8]
address = 0x04

rev = GPIO.RPI_REVISION
if rev == 2:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)   

def dustRead(pin):
    bus.write_i2c_block_data(address,1,dustRead_cmd+[pin,0,0])
    time.sleep(1)    
    bus.read_byte(address)
    number = bus.read_i2c_block_data(address,1)
    
    #millis = number[1] + (number[2] << 8) + (number[3] << 16) +  (number[4] << 24)
    #return millis
    
        #data returned in IEEE format as a float in 4 bytes 
    f=0

    for element in reversed(number[1:5]):    #data is reversed 
        hex_val=hex(element)    #Converted to hex
        #print hex_val
        try:
            h_val=hex_val[2]+hex_val[3]
        except IndexError:
            h_val='0'+hex_val[2]
        if f==0:    #Convert to char array
            h=h_val
            f=1
        else:
            h=h+h_val
    t=round(struct.unpack('!f', h.decode('hex'))[0],2)#convert the temp back to float
      
    return t      

while True:
    concentration = dustRead(8)
    print "Concentration: " + str(concentration) 
    msg = "{\"d\":{\"myName\": \"AirLevel\",\"voc\": " + str(concentration) + "}}"
    #IoTc.publish(topic, msg, 0)
    print ("sent: " + msg)
    time.sleep(30)



    
    
    
    



    
    
    
    


