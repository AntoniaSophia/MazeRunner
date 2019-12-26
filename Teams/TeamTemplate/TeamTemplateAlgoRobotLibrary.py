from subprocess import Popen
import os

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory, ".")
pythonVar = "python"


class TeamTemplateAlgoRobotLibrary(object):
    """Test library for testing business logic.
    """

    def __init__(self):
        self._result = ''
        self.processid = 0

    def teamtemplatealgo_start(self):
        executeSript = os.path.join(projectDirectory, "TeamTemplateAlgo.py")
        self.processid = Popen([pythonVar, executeSript], shell=False)

    def teamtemplatealgo_stop(self):
        self.processid.kill()
