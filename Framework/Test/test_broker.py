import pytest
import unittest
from subprocess import Popen, PIPE
import sys, os
#http://www.bx.psu.edu/~nate/pexpect/pexpect.html
from pexpect import popen_spawn
from . test_mqtt_subscriber import Sample_MQTT_Subscriber
from . test_mqtt_publisher import Sample_MQTT_Publisher
import paho.mqtt.client as mqtt
import platform

import time

pathname = os.path.dirname(__file__)        
curpath=os.path.abspath(pathname)

if platform.system() == "Windows":
    broker_path=os.path.join(curpath,"..\\MQTTBroker\\mosquitto.exe")

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"

if platform.system() != "Windows":
    mqtt_server = "mqtt.eclipse.org"

class TestMQTTBroker(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        if platform.system() == "Windows":
            print("\nStart mosquitto broker")
            broker_path=os.path.join(curpath,"..\\MQTTBroker\\mosquitto.exe")
            print(broker_path)
            assert os.path.isfile(broker_path) == True
            self.c = popen_spawn.PopenSpawn(broker_path)
            # create a new mqtt broker
        
        client=mqtt.Client()

        ##################################
        # Create a sample MQTT Publisher
        ##################################
        self.aMazePublisher = Sample_MQTT_Publisher(client)

        ##################################
        # Create a sample MQTT Subscriber
        ##################################
        self.aMazeSubscriber = Sample_MQTT_Subscriber(client)

        # start the mqtt broker
        client.loop_start()

        time.sleep(0.1)
        

    def tearDown(self):
        if platform.system() == "Windows":        
            print("\nKill mosquitto broker")
            self.c.kill(9)
            # TODO: assert for checking whether mosquitto really has been quit

    def test_feature_1(self):
        # Test feature 1
        self.aMazeSubscriber.subscribe("/maze")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze" , "clear")          # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'clear')
        self.assertEqual(receivedTopic,'/maze')


    def test_feature_2(self):
        # Test feature 2
        self.aMazeSubscriber.subscribe("/maze/#")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze/startpoint" , "42,42")          # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'42,42')
        self.assertEqual(receivedTopic,'/maze/startpoint')

    def test_feature_3(self):
        # Test feature 3
        self.aMazeSubscriber.subscribe("/maze/#")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze/endpoint" , "50,50")          # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'50,50')
        self.assertEqual(receivedTopic,'/maze/endpoint')

    def test_feature_4(self):
        # Test feature 4
        self.aMazeSubscriber.subscribe("/maze/#")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze/blocked" , "14,23")    # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'14,23')
        self.assertEqual(receivedTopic,'/maze/blocked')

    def test_feature_5(self):
        # Test feature 5
        self.aMazeSubscriber.subscribe("/maze/+/nextmove")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze/teama/nextmove" , "15,24")    # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'15,24')
        self.assertEqual(receivedTopic,'/maze/teama/nextmove')

        self.aMazePublisher.publish("/maze/teamb/nextmove" , "99,11")    # now try to get this message
        time.sleep(0.1)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'99,11')
        self.assertEqual(receivedTopic,'/maze/teamb/nextmove')

    def test_feature_6(self):
        # Test feature 6
        self.aMazeSubscriber.subscribe("/maze/+/nextmove")                 #subscribe to topic /maze
        self.aMazePublisher.publish("/maze/teama/nextmove" , "0,0")    # now try to get this message
        self.aMazePublisher.publish("/maze/teamb/nextmove" , "1,0")    # now try to get this message
        self.aMazePublisher.publish("/maze/teamc/nextmove" , "1,1")    # now try to get this message
        time.sleep(0.5)
        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'0,0')
        self.assertEqual(receivedTopic,'/maze/teama/nextmove')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,0')
        self.assertEqual(receivedTopic,'/maze/teamb/nextmove')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,1')
        self.assertEqual(receivedTopic,'/maze/teamc/nextmove')
