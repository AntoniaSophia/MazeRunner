import unittest
from test import support
from subprocess import Popen, PIPE
import sys, os
#http://www.bx.psu.edu/~nate/pexpect/pexpect.html
from pexpect import popen_spawn
from test_mqtt_subscriber import Sample_MQTT_Subscriber
from test_maze_generator import Sample_Maze_Generator
import paho.mqtt.client as mqtt


import time

pathname = os.path.dirname(sys.argv[0])        
curpath=os.path.abspath(pathname)
broker_path=os.path.join(curpath,"..\MQTTBroker\mosquitto.exe")

class TestMazeGenerator(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("\nStart mosquitto broker")
        assert os.path.isfile(broker_path) == True
        self.c = popen_spawn.PopenSpawn(broker_path)

        # create a new mqtt broker
        client=mqtt.Client()

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
        self.assertEqual(receivedTopic,'/maze/dimX')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'4')
        self.assertEqual(receivedTopic,'/maze/dimY')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'0')
        self.assertEqual(receivedTopic,'/maze/startX')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'0')
        self.assertEqual(receivedTopic,'/maze/startY')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'4')
        self.assertEqual(receivedTopic,'/maze/endX')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'3')
        self.assertEqual(receivedTopic,'/maze/endY')

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
        self.assertEqual(receivedMsg,'3,3')
        self.assertEqual(receivedTopic,'/maze/blocked')

        receivedMsg = self.aMazeSubscriber.getLastMessage()
        receivedTopic = self.aMazeSubscriber.getLastTopic()
        self.assertEqual(receivedMsg,'end')
        self.assertEqual(receivedTopic,'/maze')

def test_main():
    support.run_unittest(TestMazeGenerator)

if __name__ == '__main__':
    test_main()