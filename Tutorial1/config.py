# Poseidon Config file

# Format:
# sensorName = Pin
# If not there set it to -1 to ignore it
analogSensors = dict(
    moisture = 0,
)

#Save sensor data locally?
saveLocal = True
#Send sensor data to the MQTTBroker?
sendToCloud = True
#Send the collected sensor data to the broker after a reconnect?
sendAfterReconnect = True

#Settings for the mqtt client
mqttSettings = dict(
    #Change this to something that identifies your Client
    clientID    = 'DefaultClientName',

    #Don't change this
    server      = 'realtime.ngi.ibm.com',
    port        = 1883,
    publishTopic    = '/org/dutchcourage/poseidon/client/sensor',
)

# Location information for the GrovePi station
# Change these values!
location = dict(
    latitude         = 0,
    longitude        = 0,
)

# Interval in which values should be stored or send
# Don't set this under 30
updateInterval = 60