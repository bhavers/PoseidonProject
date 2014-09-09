import grovepi
import paho.mqtt.client as mqtt
import time, datetime
import json
import grove_barometer_lib
from sqliteClient import SQLiteClient

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

sensorValues = dict()

# Format:
# sensorName = Pin
# If not there set it to -1 to ignore it
analogSensors = dict(
    moisture = 0,
)

#Switch between local storage and sending to the cloud
saveLocal = True
sendToCloud = True

#Settings for the mqtt client
mqttSettings = dict(
    #Change this to something that identifies your Client
    clientID    = 'TheGruSensor',

    #Don't change this
    server      = 'realtime.ngi.ibm.com',
    port        = 1883,
    publishTopic    = '/org/dutchcourage/poseidon/client/sensor',
)

# Location information for the GrovePi station
# Change these values!
location = dict(
    latitude         = 48.7833,
    longitude        = 9.1833,
)

# Interval in which values should be stored or send
# Don't set this under 30
updateInterval = 60

# Read the barometer values
def readBarometerSensor():
    if barometerSensor.isAvailable():
        barometerSensor.update()
        sensorValues["temperature"] = (barometerSensor.temperature / 100.0)
        sensorValues["pressure"] = (barometerSensor.pressure / 100.0)
        sensorValues["altitude"] = (barometerSensor.altitude / 100.0)
  

#Register all analog ensors at the GrovePI
def initAnalogSensors():
    for sensor in analogSensors:
        pin = analogSensors[sensor]
        if pin >= 0:
            grovepi.pinMode(pin,"Input")

#Read all analog sensors 
def readAnalogSensors():
    for sensor in analogSensors:
        pin = analogSensors[sensor]
        if pin >= 0:
            sensorValues[sensor] = grovepi.analogRead(pin)

#Read all sensor values
def readSensors():
    readAnalogSensors()
    readBarometerSensor()
    sensorValues['timestamp'] = datetime.datetime.utcnow().isoformat()

## MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc > 0:
        print "Connection failed. RC: {}".format(rc)
    else:
        print "Connected successfully"

def on_publish(client, userdata, mid):
    print "Message {} published.".format(mid)


#For now:
#Init the sensors
initAnalogSensors()
barometerSensor = grove_barometer_lib.barometer()

if saveLocal == True:
    sqliteClient = SQLiteClient()
if sendToCloud == True:
    mqttClient = mqtt.Client(mqttSettings["clientID"])
    mqttClient.on_connect = on_connect
    mqttClient.on_publish = on_publish
    mqttClient.connect(mqttSettings["server"], mqttSettings["port"])
    mqttClient.loop()
    time.sleep(15)


while True:
    readSensors()
    if saveLocal == True :
        sqliteClient.addValues(sensorValues)
    if sendToCloud == True:
        sensorValues["clientID"] = mqttSettings["clientID"]
        sensorValues.update(location)
        mqttClient.publish(mqttSettings['publishTopic'], json.dumps(sensorValues))
        mqttClient.loop()
    print sensorValues
    sensorValues = dict()
    time.sleep(updateInterval * 60)