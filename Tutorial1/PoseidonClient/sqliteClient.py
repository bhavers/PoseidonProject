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

    def getValuesAfter(self, lastMeasurementTime):
        query = "Select * From SensorValues Where datetime(timestamp) >= datetime(?)"
        self.cursor.execute(query, lastMeasurementTime)
        return self.cursor.fetchall

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