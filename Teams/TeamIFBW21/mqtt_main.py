import os
import logging
import paho.mqtt.client as mqtt
import numpy
import argparse

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    MQTT_SERVER = os.environ['MQTTSERVER']
else:
    MQTT_SERVER = "127.0.0.1"


class MQTTTester:
    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    TARGET = 3      # the target/end position of the maze (green color)

    def __init__(self, master):
        self.master = master
        self.master.on_connect = self.onConnect
        self.master.on_message = self.onMessage
        self.master.connect(MQTT_SERVER, 1883, 60)

        self.dimCols = 0
        self.dimRows = 0
        self.startCol = 0
        self.startRow = 0
        self.endCol = 0
        self.endRow = 0
        self.grid = [[]]
        self.resultpath = []
        self.came_from = []
        print(
            "\n[TeamTemplateAlgo]: Constructor TeamTemplateAlgo successfully executed")

    def onMessage(self, master, obj, msg):
        pass

    def onConnect(self, master, obj, flags, rc):
        pass

    # loads a maze from a file pathToConfigFile
    def loadMaze(self, pathToConfigFile) -> bool:
        # check whether a function numpy.loadtxt() could be useful
        # https://numpy.org/doc/1.20/reference/generated/numpy.loadtxt.html
        exists = os.path.exists(pathToConfigFile)

        if exists:
            print("[TeamTemplateAlgo]: SUCCESS file exist: ", pathToConfigFile)
        else:
            print("[TeamTemplateAlgo]: ERROR file not exist ", pathToConfigFile)
            return False
        try:
            self.grid = numpy.loadtxt(
                pathToConfigFile, dtype='int64', delimiter=",")
            (self.dimRows, self.dimCols) = self.grid.shape

            [self.endRow, self.endCol] = numpy.concatenate(
                numpy.where(self.grid == self.TARGET)).tolist()
            [self.startRow, self.startCol] = numpy.concatenate(
                numpy.where(self.grid == self.START)).tolist()

        except ValueError as err:
            print(f"Error in Maze please check: {err}", pathToConfigFile)
            return False
        return True

    def publish(self, topic, message=None, qos=0, retain=False):
        """Generic method to publish MQTT messages"""
        print("[MazeSolverClient]: Published message: ", topic, " --> ", message)
        self.master.publish(topic, message, qos, retain)
        # time.sleep(0.01)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The maze as text file"
    )
    args = parser.parse_args()

    MQTT_CLIENT = mqtt.Client()
    tester = MQTTTester(MQTT_CLIENT)
    logging.basicConfig(level=logging.ERROR)
    LOGGER = logging.getLogger(__name__)
    MQTT_CLIENT.enable_logger(LOGGER)
    tester.loadMaze(args.input_file)

    tester.publish("/maze", "clear")
    tester.publish("/maze", "start")
    tester.publish("/maze/dimRow", str(tester.dimRows))
    tester.publish("/maze/dimCol", str(tester.dimCols))
    tester.publish("/maze/startRow", str(tester.startRow))
    tester.publish("/maze/startCol", str(tester.startCol))
    tester.publish("/maze/endRow", str(tester.endRow))
    tester.publish("/maze/endCol", str(tester.endCol))

    for y in range(tester.dimRows):
        for x in range(tester.dimCols):
            if tester.grid[y][x] == tester.OBSTACLE:
                tester.publish("/maze/blocked", f'{y},{x}')

    tester.publish("/maze", "solve")
    tester.publish("/maze", "end")
