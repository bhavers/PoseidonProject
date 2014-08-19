# Settings file for the Poseidon Client
poseidonSettings = dict(
	#Interval to read sensors and publish data in minutes
	updateIntervall = 2,
	
	#Location information
	#Used to display your data on a Map
	#location = dict(
	#	country 	= "Germany",
	#	city 		= "Stuttgart",
	#	street 	= "Koenigstrasse 123",
	#),
	#Alternative:
    location = dict(
        lat 		= 48.7833,
        long		= 9.1833,
    ),


	## Settings for the MQTT Client
	### Name			Description												Default values 			Comments
	###
	### server 			IP Adress or hostname of the MQTT server				"127.0.0.1"
	### port 			Port on which the MQTT server listens					1883
	### clientID 		The ID for this client									"TestClient"
	### controlTopic 	Topic on which controls can be send to this client 		"my/ctl/topic"			Not used currently
	### publishTopic 	Topic on which this client publishes the sensor values 	"my/pub/topic"
	### qos 			Quality of Service parameter 							0						Please refer to http://mosquitto.org/man/mqtt-7.html
	mosquittoSettings = dict(
		server	 	= '127.0.0.1',
		port 		= 12000,
		clientID 	= 'TestClient',
		controlTopic 	= 'yay/super/topic',
		publishTopic 	= 'yay/geiles/topic',
		qos 		= 0,
	),

	## Settings for controlling the GrovePi
	### Available Sensors:
	### Name 									Key				Port Type
	###
	### Air Quality Sensor								Air				Analog
	### Light Sensor								Light				Analog
	### Sound	Sensor								Sound				Analog
	### Temperatur and Humidity Sensor						DHT11				Digital
	### Temperatur and Humidity Sensor pro						DHT22				Digital
	### Water Sensor - Analog Port							Water_Analog			Analog
	### Water Sensor - Digital Port						Water_Digital			Digital
	###
	### To register new Sensors add their Key and the port number to the list
	### <Key> = <Port Number>,
	### Air = 1
	### Air Sensor is plugged in at Analog Port 1

	groveSettings = dict(
		DHT11 		= 4,
		Water_Digital	= 3,
		Light		= 2,	
		Sound 		= 0,
		Air 		= 1,
	),
)
