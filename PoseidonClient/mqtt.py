import mosquitto


class MqttClient(object):
    def __str___(self):
        return "Mosquitto Client connected to {} , subscribed to topics {} and publishes to topic {}".format(
            self.config["server"], self.config["controlTopic"], self.config["publishTopic"])

    def publish(self, message):
        self.client.publish(self.config["publishTopic"], str(message), self.config["qos"])

    def loop(self):
        self.client.loop()

    # # Callbacks
    def _on_connect(self, mosq, obj, rc):
        if rc == 0:
            print "Connected successfully."
        else:
            print "Connection failed. RC: {}".format(rc)

    def _on_disconnect(self, mosq, obj, rc):
        print "Disconnected successfully."

    def _on_message(self, mosq, obj, msg):
        print "Message received on topic {} with QoS {} and payload {}".format(msg.topic, msg.qos, msg.payload)

    def _on_publish(self, mosq, obj, mid):
        print "Message {} published.".format(mid)

    def _on_subscribe(self,mosq, obj, mid, qos_list):
        print("Subscribe with mid "+str(mid)+" received.")

    def _on_unsubscribe(self,mosq, obj, mid):
        print "Unsubscribe with mid  received.".format(mid)


    def __init__(self, mqttConfig):
        self.config = mqttConfig
        self.client = mosquitto.Mosquitto(self.config["clientID"])

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        self.client.on_unsubscribe = self._on_unsubscribe

        self.client.connect(self.config["server"], self.config["port"])
        self.client.subscribe(self.config["controlTopic"], self.config["qos"])
