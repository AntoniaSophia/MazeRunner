import paho.mqtt.client as mqtt
import time

class Sample_MQTT_Publisher:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        #print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)


    def __init__(self,master):
        print("Constructor Sample_MQTT_Publisher")
        self.master=master
        self.master.on_connect=self.onConnect
        self.master.connect("127.0.0.1",1883,60)

