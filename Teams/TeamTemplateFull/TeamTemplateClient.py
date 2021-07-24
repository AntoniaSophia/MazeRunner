"""
This class is the template class for the MQTT client which receives MQTT messages
and sends MQTT messages
"""
import os
import logging
import paho.mqtt.client as mqtt


if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"

# HINT: it might be a good idea to copy this file into your team folder, e.g. TeamA
# HINT: it might be good idea to rename both the file and the class name


class TeamTemplateClient:

    # initialize the MQTT client
    def __init__(self, master):
        # TODO: this is you job now :-)

        self.master = master
        self.name = "TeamTemplateClient"

        # HINT: here you should register the onConnect and onMessage callback functions
        #       it might be a good idea to look into file Framework\Test\test_mqtt_publisher.py

        self.master.connect(mqtt_server, 1883, 60)

        print("\n[TeamTemplateClient]: Constructor MazeSolverClient successfully executed...")
        # This MQTT client forwards the requests, so you need a link to the solver
        # HINT: don't forget to create your algorithm class here, e.g.
        # self.solver = MazeSolverAlgoTemplate()

    # Implement MQTT publishing function

    def publish(self, topic, message=None, qos=0, retain=False):
        # TODO: this is you job now :-)
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_publisher.py
        pass

    # Implement MQTT receive message function

    def onMessage(self, master, obj, msg):
        # pylint: disable=unused-argument
        # TODO: this is you job now :-)
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_subscriber.py
        print("[TeamTemplateClient]: Received message:", str(msg.topic), " --> ", str(msg.payload.decode("utf-8")))
        # pass

    # Implement MQTT onConnecr function
    def onConnect(self, master, obj, flags, rc):
        # TODO: this is you job now :-)
        # HINT: it might be a good idea to look into file Framework\Test\test_mqtt_subscriber.py

        # print("\n[TeamTemplateClient]: MazeSolverClient successfully subscribed to messages...")
        pass

    # Initiate the solving process of the maze solver

    def solveMaze(self):
        # TODO: this is you job now :-)

        # HINT:  don't forget to publish the results, e.g.
        # self.publish("/maze/go" , resultString)
        pass


if __name__ == '__main__':
    mqttclient = mqtt.Client()
    # HINT: maybe you rename the MazeSolverAlgoTemplate class ?
    solverClient = TeamTemplateClient(mqttclient)
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    mqttclient.enable_logger(logger)
    solverClient.master.loop_forever()
