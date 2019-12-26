from subprocess import Popen
import os

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory, "../..")


class GeneratorLibrary(object):
    """Test library for testing *Calculator* business logic.

    Interacts with the calculator directly using its ``push`` method.
    """

    def __init__(self):
        self._result = ''
        self.generatorpid = 0

    def generator_action(self, width, height, complexity, density, stralgo):
        executeSript = os.path.join(
            projectDirectory, "Framework", "GeneratorAlternative", "MazeGeneratorClient.py")
        self.generatorpid = Popen(['python', executeSript, "--width="+str(width), "--height="+str(
            height), "--complexity="+str(complexity), "--density="+str(density),
            "--algo=", stralgo], shell=False)
        self.generatorpid.communicate()
        print("Generator run")

    def generator_load(self, filename):
        executeSript = os.path.join(
            projectDirectory, "Framework", "GeneratorAlternative", "MazeGeneratorClient.py")
        self.generatorpid = Popen(['python', executeSript, "--ifile="+str(filename)], shell=False)
        self.generatorpid.communicate()
        print("Generator run")

    # def push_button(self, button):
    #     """Pushes the specified ``button``.

    #     The given value is passed to the calculator directly. Valid buttons
    #     are everything that the calculator accepts.

    #     Examples:
    #     | Push Button | 1 |
    #     | Push Button | C |

    #     Use `Push Buttons` if you need to input longer expressions.
    #     """
    #     self._result = self._calc.push(button)

    # def push_buttons(self, buttons):
    #     """Pushes the specified ``buttons``.

    #     Uses `Push Button` to push all the buttons that must be given as
    #     a single string. Possible spaces are ignored.

    #     Example:
    #     | Push Buttons | 1 + 2 = |
    #     """
    #     for button in buttons.replace(' ', ''):
    #         self.push_button(button)

    # def result_should_be(self, expected):
    #     """Verifies that the current result is ``expected``.

    #     Example:
    #     | Push Buttons     | 1 + 2 = |
    #     | Result Should Be | 3       |
    #     """
    #     if self._result != expected:
    #         raise AssertionError('%s != %s' % (self._result, expected))

    # def should_cause_error(self, expression):
    #     """Verifies that calculating the given ``expression`` causes an error.

    #     The error message is returned and can be verified using, for example,
    #     `Should Be Equal` or other keywords in `BuiltIn` library.

    #     Examples:
    #     | Should Cause Error | invalid            |                   |
    #     | ${error} =         | Should Cause Error | 1 / 0             |
    #     | Should Be Equal    | ${error}           | Division by zero. |
    #     """
    #     try:
    #         self.push_buttons(expression)
    #     except CalculationError as err:
    #         return str(err)
    #     else:
    #         raise AssertionError("'%s' should have caused an error."
    #                              % expression)
