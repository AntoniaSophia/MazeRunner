from subprocess import Popen
import os

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory, "../../..")
pythonVar = "python"


class AStarSusannaSolverLibrary(object):
    """Test library for testing *Calculator* business logic.

    Interacts with the calculator directly using its ``push`` method.
    """

    def __init__(self):
        self._result = ''
        self.astarpid = 0

    def astarsusanna_start(self):
        executeSript = os.path.join(projectDirectory, "Teams", "ReferenceSolutionBreadthFirst", "MazeSolverClient.py")
        self.breadthfirstpid = Popen([pythonVar, executeSript], shell=False)

    def astarsusanna_stop(self):
        self.breadthfirstpid.kill()
