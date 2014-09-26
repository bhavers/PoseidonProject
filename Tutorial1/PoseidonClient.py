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

sensorValues = dict()

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
    readBarometerSensor()
    sensorValues['timestamp'],lastMeasurementTime = datetime.datetime.utcnow().isoformat()

def processData():
    print sensorValues
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
initAnalogSensors()
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
    processData()
    if config.sendAfterReconnect == True and hasDisconnected == True:
        sendBulkData()
    time.sleep(config.updateInterval * 60)
