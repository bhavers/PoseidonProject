# Poseidon Config file



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