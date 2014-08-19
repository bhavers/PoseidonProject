from grove import GrovePi
from mqtt import MqttClient
from sqliteClient import SQLiteClient
import configurationFile
import time
import formater

class PoseidonClient(object):
    def __init__(self):
        self.config = configurationFile.poseidonSettings
        self.grove = GrovePi(self.config["groveSettings"])
        self.sqlClient = SQLiteClient()
        self.mqtt = MqttClient(self.config["mosquittoSettings"])
        self.formatter = formater.jsonFormater(self.config["location"],self.config["mosquittoSettings"]["clientID"])



    def loop(self):
        while True:
            sensorData = self.grove.readSensors()
            json = self.formatter.sensorToJSON(sensorData, time.time())
            #print sensorData
            #self.sqlClient.addValues(sensorData)
            self.mqtt.publish(json)
            time.sleep(60*self.config["updateIntervall"])


if __name__ == "__main__":
    client = PoseidonClient()
    client.loop()
