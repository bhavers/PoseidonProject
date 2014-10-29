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
# 
# Description: Poseidon Config file

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