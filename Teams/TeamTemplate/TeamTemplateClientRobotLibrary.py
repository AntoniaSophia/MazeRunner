import sys
from subprocess import Popen
import os
import threading
import time
import platform
import paho.mqtt.client as paho

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory, ".")
pythonVar = "python"


class TeamTemplateClientRobotLibrary(object):
    """Test library for testing business logic.
    """

    def __init__(self):
        self._result = ''
        self.processid = 0

    def teamtemplateclient_start(self):
        executeSript = os.path.join(projectDirectory, "TeamTemplateClient.py")
        self.processid = Popen([pythonVar, executeSript], shell=False)

    def teamtemplateclient_stop(self):
        self.processid.kill()
