import paho.mqtt.client as mqtt
import time

import os

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"

if platform.system() != "Windows":
    mqtt_server = "mqtt.eclipse.org"

class Sample_MQTT_Subscriber:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        #print("Sub: Connnect to mqtt-broker")
        pass

    def onMessage(self, master, obj, msg):
        self.last_messages.insert(0,str(msg.payload.decode("utf-8")))
        self.last_topics.insert(0,str(msg.topic))
        print("Received message:", str(msg.topic) , " --> " , str(msg.payload.decode("utf-8")))

    def getLastMessage(self):
        #return self.last_message
        return self.last_messages.pop()

    def getLastTopic(self):
        return self.last_topics.pop()

    def subscribe(self, topic):
        self.master.subscribe(topic)

    def __init__(self,master):
        print("Constructor Sample_MQTT_Subscriber")
        self.last_messages=[]
        self.last_topics=[]
        self.master=master
        self.master.on_connect=self.onConnect
        self.master.on_message=self.onMessage
        self.master.connect(mqtt_server,1883,60)
