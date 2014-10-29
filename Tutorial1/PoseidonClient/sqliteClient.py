import sqlite3 as lite
import sys


class SQLiteClient:

    def addValues(self, values):
        query = "Insert Into SensorValues (timestamp, moisture, pressure, altitude, temperature) Values (?, ?, ?, ?, ?)" 
        self.cursor.execute(query, values.values())
        self.connection.commit()

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
            "CREATE TABLE IF NOT EXISTS SensorValues(ID INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "timestamp TEXT, moisture INT, pressure REAL, altitude REAL, temperature REAL)")
        self.connection.commit()
    def __init__(self):
        try:
            self.connection = lite.connect('Poseidon.db')
            self.cursor = self.connection.cursor()
            self._createTable()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)