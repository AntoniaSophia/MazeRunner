import paho.mqtt.client as mqtt
import time

class client1:

    def on_connect(self, master, obj, flags, rc):
        self.master.subscribe('/maze/*')
        print("Connnect to mqtt-broker")


    def on_message(self, master, obj, msg):
        print(str(msg.payload))

    def __init__(self,master):
        print("Constructor client1")
        self.master=master
        self.master.on_connect=self.on_connect
        self.master.on_message=self.on_message
        self.master.connect("127.0.0.1",1883,60)


class demo:
    def __init__(self):
        print("Constructor demo")
        self.client=mqtt.Client()
        self.ob1=client1(self.client)
        self.client.loop_start()
    
tester = demo()

while True: 
    time.sleep(0.2)