# Copyright Dutch Courage Foundation 2014  
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import grovepi
import paho.mqtt.client as mqtt
import time, datetime
import json
import grove_barometer_lib
import config
import sys
from sqliteClient import SQLiteClient


sys.stdout = open('poseidon.log', 'w', 1)


##########################
# Needed python libaries:#
# sqllite                #
# paho-mqtt              #
##########################
# Install with :         #
# pip install <lib name> #
##########################

#############################
# Variables to change :     #
# - saveLocal               #
# - sendToCloud             #
# - location                #
# - mqttSettings            #
# - analogSensors           #
#############################

#TODO:
# Add functions for digital and I2C sensors 
# If connection lost retry and send bulk information since last send

# Read the barometer values
def readBarometerSensor():
    if barometerSensor.isAvailable():
        barometerSensor.update()
        sensorValues["temperature"] = (barometerSensor.temperature / 100.0)
        sensorValues["pressure"] = (barometerSensor.pressure / 100.0)
        sensorValues["altitude"] = (barometerSensor.altitude / 100.0)
  

#Register all analog ensors at the GrovePI
def initAnalogSensors():
    for sensor in config.analogSensors:
        pin = config.analogSensors[sensor]
        if pin >= 0:
            grovepi.pinMode(pin,"Input")

#Read all analog sensors 
def readAnalogSensors():
    for sensor in config.analogSensors:
        pin = config.analogSensors[sensor]
        if pin >= 0:
            sensorValues[sensor] = grovepi.analogRead(pin)

#Read all sensor values
def readSensors():
    readAnalogSensors()
    if config.barometerSensor == True:
        readBarometerSensor()
    sensorValues['timestamp'] = datetime.datetime.utcnow().isoformat()
    lastMeasurementTime = datetime.datetime.utcnow().isoformat()

def processData():
    global sensorValues
    if config.saveLocal == True :
        sqliteClient.addValues(sensorValues)
    if config.sendToCloud == True:
        sensorValues["clientID"] = config.mqttSettings["clientID"]
        sensorValues.update(config.location)
        mqttClient.publish(config.mqttSettings['publishTopic'], json.dumps(sensorValues))
    sensorValues = dict()

def sendBulkData():
    for valueSet in sqliteClient.getValuesAfter(lastMeasurementTime):
        sensorValues = valueSet
        processData()
    hasDisconnected = False

## MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print "Connection failed. RC: {}".format(rc)
    else:
        print "Connected successfully"

def on_publish(client, userdata, mid):
    print "Message {} published.".format(mid)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print "Client disconnected unexpectedly, trying to reconnect."
        hasDisconnected = True
        mqttClient.reconnect()

#Init the sensors
sensorValues = dict()
initAnalogSensors()
if config.barometerSensor == True :
    barometerSensor = grove_barometer_lib.barometer()

lastMeasurementTime = 0

if config.sendAfterReconnect == True:
    hasDisconnected = False
if config.saveLocal == True:
    sqliteClient = SQLiteClient()
if config.sendToCloud == True:
    mqttClient = mqtt.Client(config.mqttSettings["clientID"])
    mqttClient.on_connect = on_connect
    mqttClient.on_publish = on_publish
    mqttClient.on_disconnect = on_disconnect
    mqttClient.loop_start()
    mqttClient.connect(config.mqttSettings["server"], config.mqttSettings["port"])



while True:
    readSensors()
    print sensorValues
    processData()
    if config.sendAfterReconnect == True and hasDisconnected == True:
        sendBulkData()
    time.sleep(config.updateInterval * 60)
