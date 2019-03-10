import paho.mqtt.client as mqtt
import time

class PubTest:

    def on_connect(self, master, obj, flags, rc):
        print("Pub: Connnect to mqtt-broker")

    def __init__(self,master):
        print("Constructor SubTest")
        self.master=master
        self.master.on_connect=self.on_connect
        self.master.connect("127.0.0.1",1883,60)
    
    def sendMessage(self, topic, message):
        self.master.publish(topic, message)

class PubTestDemo:
    def __init__(self):
        print("Constructor demo")
        self.client=mqtt.Client()
        self.ob1=PubTest(self.client)
        self.client.loop_start()

    def sendMessage(self, topic, message):
        self.ob1.sendMessage(topic, message)

class SubTest:

    def on_connect(self, master, obj, flags, rc):
        self.master.subscribe(self.topic)
        print("Sub: Connnect to mqtt-broker")


    def on_message(self, master, obj, msg):
        print(str(msg.payload))
        self.last_message=str(msg.payload.decode("utf-8"))

    def __init__(self,master, topic):
        print("Constructor SubTest")
        self.last_message=""
        self.master=master
        self.topic=topic
        self.master.on_connect=self.on_connect
        self.master.on_message=self.on_message
        self.master.connect("127.0.0.1",1883,60)


class SubTestDemo:
    
    def __init__(self, topic):
        print("Constructor demo")
        self.client=mqtt.Client()
        self.ob1=SubTest(self.client, topic)
        self.client.loop_start()

    def getlastmessage(self):
        return self.ob1.last_message


def main():
    testerSub = SubTestDemo()
    testerPub = PubTestDemo()

    while True: 
        testerPub.sendMessage("/maze","Hallo")
        time.sleep(0.2)


if __name__ == "__main__":
    main()

