import grovepi
import paho-mqtt
import time
import grove_barometer_lib


#TODO:
# Rewrite mqtt wrapper
# Add functions for digital and I2C sensors 
# Add JSON formatter for all values

sensorValues = dict()

# Format:
# sensorName = Pin
# If not there set it to -1 to ignore it
analogSensors = dict(
    light = 0,
    air = 1,
    moisture = -1,
)

barometerSensor = grove_barometer_lib.barometer()

mqttSettings = dict(
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

def readBarometerSensor():
    if barometerSensor.isAvailable()
        barometerSensor.update()
        sensorValues["temperatur"] = (barometerSensor.temperature / 100.0)
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


## MQTT Callbacks
def _on_connect(mosq, obj, rc):
    if rc < 0:
        print "Connection failed. RC: {}".format(rc)

def _on_publish(mosq, obj, mid):
    print "Message {} published.".format(mid)


def intitMQTT():
    mqttClient = mqtt.Client(mqttSettings["clientID"])

    mqttClient.on_connect = self._on_connect
    mqttClient.on_publish = self._on_publish

    mqttClient.connect(mqttSettings["server"], mqttSettings["port"])



#intitMQTT()
initAnalogSensors()

#For now: Print all the analog sensor values
while True:
    readAnalogSensors()
    readBarometerSensor()
    print sensorValues
    time.sleep(2)


