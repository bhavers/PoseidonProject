import json
import datetime
import time

class jsonFormater(object):
    def __init__(self,location, clientID):
        self.location = location
        self.clientID = clientID

    def sensorToJSON(self,values, timestamp):
        values["location"] = self.location
        values["timestamp"] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        values["clientID"] = self.clientID
        return json.dumps(values)