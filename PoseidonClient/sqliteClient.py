import sqlite3 as lite
import sys


class SQLiteClient:

    def addValues(self, values):
        query = "Insert Into SensorValues (%s) Values (%s)" % (",".join(values),",".join(['?']*len(values)))
        print query
        self.cursor.execute(query,values.values())

    def getAllValues(self):
        query = "SELECT * FROM SensorValues"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getLatestValues(self):
        query = "Select * From SensorValues ORDER BY ID DESC"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def _createTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS SensorValues(ID INTEGER PRIMARY KEY AUTOINCREMENT, TimeStamp DATETIME, Air INT, Light INT, Sound INT, DHT11_humidity REAL, DHT11_temp REAL, DHT22_humidity REAL, DHT22_temp REAL, Water_Digital INT,Water_Analog INT)")

    def __init__(self):
        try:
            self.connection = lite.connect('Poseidon.db')
            self.cursor = self.connection.cursor()
            self._createTable()
        except lite.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)