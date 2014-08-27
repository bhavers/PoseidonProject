import grovepi
from mqtt import MqttClient
import time


#TODO:
# Rewrite mqtt wrapper
# Add functions for digital and I2C sensors 
# Add JSON formatter for all values
# Add Barometer to grovepi lib (Send Pull request to dexterInd)
#
#

sensorValues = dict()

analogSensors = dict(
    light = 0,
    air = 1,
)
digitalSensors = dict(
)

I2CSensors = dict(
)

mosquittoSettings = dict(
    server      = '127.0.0.1',
    port        = 12000,
    clientID    = 'TestClient',
    controlTopic    = 'yay/super/topic',
    publishTopic    = 'yay/geiles/topic',
    qos         = 0,
)

location = dict(
    lat         = 48.7833,
    long        = 9.1833,
)

updateInterval = 15

#Register all analog ensors at the GrovePI
def initAnalogSensors():
    for sensor in analogSensors:
        grovepi.pinMode(analogSensors[sensor],"Input")
#Read all analog sensors 
def readAnalogSensors():
    for sensor in analogSensors:
        sensorValues[sensor] = grovepi.analogRead(analogSensors[sensor])

initAnalogSensors()

#For now: Print all the analog sensor values
while True:
    readAnalogSensors()
    print sensorValues
    time.sleep(2)


