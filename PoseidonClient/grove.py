import grovepi
from math import isnan
import ast

### Wrapper for the GrovePi Libary
### Provides functions to easily initialize and read sensor values
### Refer to configurationFile.py for setting up the needed information.
### 
class GrovePi(object):

	def _initAir(self, pin):
		return grovepi.pinMode(pin,"INPUT")

	def _initLight(self, pin):
		return grovepi.pinMode(pin,"INPUT")

	def _initSound(self, pin):
		return grovepi.pinMode(pin,"INPUT")

	def _initDHT11(self, pin):
		return 1
	
	def _initDHT22(self, pin):
		return 1
	
	def _initWater_Analog(self, pin):
		return grovepi.pinMode(pin,"INPUT")

	def _initWater_Digital(self, pin):
		return grovepi.pinMode(pin,"INPUT")

#	Function to read all registered sensors

	def _readSound(self,pin):
		try:
			return grovepi.analogRead(pin)
		except IOError:
			print "Error while reading the sound sensor."

	def _readAir(self,pin):
		try:
			return grovepi.analogRead(pin)
		except IOError:
			print "Error while reading the air quality sensor."

	def _readDHT11(self,pin):
		try:
			temp, humidity = grovepi.dht(pin,0)
			if isnan(temp) and isnan(humidity):
				print "Error while reading the DHT11 sensor. (Firmware >= 1.1?)"
				return -1, -1
			elif temp is None or humidity is None:
				print "Error while reading the DHT11 sensor"
				return -1, -1
			else:
				return temp, humidity
		except IOError:
			print "Error while reading the DHT11 sensor."
			return -1, -1

	def _readDHT22(self,pin):
		try:
			temp, humidity = grovepi.dht(pin,1)
			if isnan(temp) and isnan(humidity):
				print "Error while reading the DHT22 sensor. (Firmware >= 1.1?)"
				return -1, -1
			elif temp is None or humidity is None:
				print "Error while reading the DHT22 sensor."
				return -1, -1
			else:	
				return temp, humidity
		except IOError:
			print "Error while reading the DHT22 sensor."

	def _readWater_Analog(self,pin):
		try:
			return grovepi.analogRead(pin)
		except IOError:
			print "Error while reading the sound sensor."

	def _readWater_Digital(self,pin):
		try:
			return grovepi.digitalRead(pin)
		except IOError:
			print "Error while reading the sound sensor."

	def _readLight(self, pin):
		try:
        		return grovepi.analogRead(pin)
		except IOError:
			print "Error while reading the sound sensor."

	### Function to read all configured sensor values
	### Uses the dict from the init function
	def readSensors(self):
		values = dict()
		for sensor in self.config:
			if "DHT" in sensor:
				[temp, humidity] = getattr(self,'_read{}'.format(sensor))(self.config[sensor])
				values[sensor+'_temp'] = temp
				values[sensor+'_humidity'] = humidity
			else:
				values[sensor] = getattr(self,'_read{}'.format(sensor))(self.config[sensor])
		return values

	### Function to initialize the used pins
	### This function gets called automaically when creating an GrovePi object
	### Expects a dict of form:
	### var = dict {"Sensor1Name":pinNumnber,"Sensor2Name":pinNumber}
	### Also see the configurationFile.py for the naming schema of the sensors   
	def __init__(self, groveConfig):
		self.config = groveConfig
		for sensor in self.config:
			returnValue = getattr(self,'_init{}'.format(sensor))(self.config[sensor])
			if returnValue != 1 :
				raise RuntimeError("Could not initialize sensor {}".format(sensor))	
