"""This is an implementation of an MQTT client which
    - receives mazes
    - sends back solution steps from a maze solver
    It is an implementation of TeamTemplate/TeamTemplateClient"""
import os
import logging
import paho.mqtt.client as mqtt
from IFBW21Algo import IFBW21Algo


if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    MQTT_SERVER = os.environ['MQTTSERVER']
else:
    MQTT_SERVER = "127.0.0.1"


class MQTTClientAlgo:
    """This is an implementation of an MQTT client which
        - receives mazes
        - sends back solution steps from a maze solver
        It is an implementation of TeamTemplate/TeamTemplateClient"""
    def __init__(self, master):
        self.master = master
        self.master.on_connect = self.onConnect
        self.master.on_message = self.onMessage
        self.master.connect(MQTT_SERVER, 1883, 60)

        self.solver = IFBW21Algo()
        self.solver.master = self.master

    def onMessage(self, master, obj, msg):
        # pylint: disable=unused-argument
        """This is the onMessage method which has to be implemented \
            in order to serve as MQTT client - don't forget to register it!
            In this method we define how the MQTT messages we receive shall be processed"""
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        print("[MazeSolverClient]: Received message: ", topic, " --> ", payload)
        if topic == "/maze":
            if payload == "clear":
                self.solver.clearMaze()
            elif payload == "solve":
                self.solveMaze()
            elif payload == "end":
                self.solver.endMaze()
                self.solver.printMaze()
            else:
                pass
        elif topic == "/maze/dimRow":
            self.solver.setDimRows(int(payload))
            self.solver.startMaze()
        elif topic == "/maze/dimCol":
            self.solver.setDimCols(int(payload))
            self.solver.startMaze()
        elif topic == "/maze/startCol":
            self.solver.setStartCol(int(payload))
        elif topic == "/maze/startRow":
            self.solver.setStartRow(int(payload))
        elif topic == "/maze/endCol":
            self.solver.setEndCol(int(payload))
        elif topic == "/maze/endRow":
            self.solver.setEndRow(int(payload))
        elif topic == "/maze/blocked":
            cell = payload.split(",")
            print(cell)
            self.solver.setBlocked(int(cell[0]), int(cell[1]))
        else:
            pass

    def onConnect(self, master, obj, flags, rc):
        # pylint: disable=unused-argument
        """This is the onConnect method which has to be implemented \
            in order to serve as MQTT client - don't forget to register it!
            In this method we define which MQTT messages we would like to receive"""
        self.master.subscribe("/maze")
        self.master.subscribe("/maze/dimRow")
        self.master.subscribe("/maze/dimCol")
        self.master.subscribe("/maze/startCol")
        self.master.subscribe("/maze/startRow")
        self.master.subscribe("/maze/endCol")
        self.master.subscribe("/maze/endRow")
        self.master.subscribe("/maze/blocked")

    def logMsg(self, msg):
        """Method to publish log messages via MQTT"""
        self.publish("/logging/Solver", msg)

    def publish(self, topic, message=None, qos=1, retain=False):
        """Generic method to publish MQTT messages"""
        print("[MazeSolverClient]: Published message: ", topic, " --> ", message)
        self.master.publish(topic, message, qos, retain)

    def solveMaze(self):
        """Command to start solving the maze """
        for step in self.solver.solveMaze():
            step_str = '{},{}'.format(step[0], step[1])

            self.publish("/maze/go", step_str)


if __name__ == '__main__':
    MQTT_CLIENT = mqtt.Client()
    SOLVER_CLIENT = MQTTClientAlgo(MQTT_CLIENT)
    logging.basicConfig(level=logging.ERROR)
    LOGGER = logging.getLogger(__name__)
    MQTT_CLIENT.enable_logger(LOGGER)
    SOLVER_CLIENT.master.loop_forever()
