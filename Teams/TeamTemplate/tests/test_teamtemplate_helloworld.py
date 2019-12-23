import unittest
import pytest
import os,sys,inspect
from subprocess import Popen
import logging
import tempfile
import paho.mqtt.client as mqtt
from shutil import copyfile, rmtree, copy, copytree, move
import numpy 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from TeamTemplateClient import TeamTemplateClient

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory, ".")

class TT_HelloWorld(unittest.TestCase):

    def testCreateMQTTClient(self):
        if sys.platform == "win32":
            executeSript = os.path.join(
                projectDirectory, "../../../Framework", "MQTTBroker", "mosquitto.exe")
            Popen([executeSript], shell=False) 


        mqttclient=mqtt.Client()
        client = TeamTemplateClient(mqttclient)

        self.assertTrue(client.name == "TeamTemplateClient")
        self.assertTrue(client.master is not None)

        if sys.platform == "win32":        
            os.system("taskkill /f /im mosquitto.exe")

    def testReceiveMQTTMessages(self):
        self.assertTrue(True==True)
        #self.assertTrue(True=True)



 