import unittest
import pytest
from subprocess import Popen, PIPE
import sys, os
#http://www.bx.psu.edu/~nate/pexpect/pexpect.html
from pexpect import popen_spawn
from . test_mqtt_subscriber import Sample_MQTT_Subscriber
from . test_maze_generator import Sample_Maze_Generator
import paho.mqtt.client as mqtt
import platform

import time

pathname = os.path.dirname(__file__)        
curpath=os.path.abspath(pathname)

if platform.system() == "Windows":
    broker_path=os.path.join(curpath,"..\\MQTTBroker\\mosquitto.exe")
else:
    broker_path=os.path.join("mosquitto")

class TestMazeGenerator(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        if platform.system() == "Windows":
            print("\nStart mosquitto broker")
            assert os.path.isfile(broker_path) == True
            self.c = popen_spawn.PopenSpawn(broker_path)

            # create a new mqtt broker
        client=mqtt.Client()

        if platform.system() != "Windows":
            client.connect("mqtt.eclipse.org", 1883, 60)

        ##################################
        # Create a sample MQTT Publisher
        ##################################
        self.aMazePublisher = Sample_Maze_Generator(client)

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
        self.aMazeSubscriber.subscribe("/maze/#")                 #subscribe to topic /maze
        
        self.aMazePublisher.sendMaze()
        time.sleep(1)

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'clear')
        self.assertEqual(receivedTopic,'/maze')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'start')
        self.assertEqual(receivedTopic,'/maze')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'5')
        self.assertEqual(receivedTopic,'/maze/dimCol')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'5')
        self.assertEqual(receivedTopic,'/maze/dimRow')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'0')
        self.assertEqual(receivedTopic,'/maze/startCol')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'0')
        self.assertEqual(receivedTopic,'/maze/startRow')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'4')
        self.assertEqual(receivedTopic,'/maze/endCol')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'4')
        self.assertEqual(receivedTopic,'/maze/endRow')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,1')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,2')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,3')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'1,4')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'2,1')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'2,3')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'3,1')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'4,3')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'end')
        self.assertEqual(receivedTopic,'/maze')
