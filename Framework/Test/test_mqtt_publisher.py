import os
import platform

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"


if platform.system() != "Windows":
    mqtt_server = "mqtt.eclipse.org"


class Sample_MQTT_Publisher:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        # print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: ", topic, " --> ", message)
        self.master.publish(topic, message, qos, retain)

    def __init__(self, master):
        print("Constructor Sample_MQTT_Publisher")
        self.master = master
        self.master.on_connect = self.onConnect
        self.master.connect(mqtt_server, 1883, 60)
