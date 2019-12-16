import paho.mqtt.client as mqtt
import time
import array as arr
from MazeSolverAlgoBreadthFirst import MazeSolverAlgoBreadthFirst
import os
import logging

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"
    
class MazeSolverClient:

    def __init__(self,master):
        self.master=master
        self.master.on_connect=self.onConnect
        self.master.on_message=self.onMessage
        self.master.connect(mqtt_server,1883,60)

        self.solver = MazeSolverAlgoBreadthFirst()

    def onMessage(self, master, obj, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        print("Received message: " , topic , " --> " , payload)
        if topic=="/maze":
            if payload == "clear":
                self.solver.clearMaze()
            elif payload == "start":
                self.solver.startMaze()
            elif payload == "solve":
                self.solveMaze()                
            elif payload == "end":
                self.solver.endMaze()
                self.solver.printMaze()
            else:
                pass
        elif topic=="/maze/dimRow":
            self.solver.setDimRows(int(payload))
            self.solver.startMaze(self.solver.dimRows, self.solver.dimColumns)
        elif topic=="/maze/dimCol":
            self.solver.setDimCols(int(payload))
            self.solver.startMaze(self.solver.dimRows, self.solver.dimColumns)
        elif topic=="/maze/startCol":
            self.solver.setStartCol(int(payload))
        elif topic=="/maze/startRow":
            self.solver.setStartRow(int(payload))
        elif topic=="/maze/endCol":
            self.solver.setEndCol(int(payload))
        elif topic=="/maze/endRow":
            self.solver.setEndRow(int(payload))
        elif topic=="/maze/blocked":
            cell = payload.split(",")
            self.solver.setBlocked(int(cell[0]),int(cell[1]))
        else:
            pass

    def onConnect(self, master, obj, flags, rc):
        self.master.subscribe("/maze" )
        self.master.subscribe("/maze/dimRow" )
        self.master.subscribe("/maze/dimCol" )
        self.master.subscribe("/maze/startCol" )
        self.master.subscribe("/maze/startRow" )
        self.master.subscribe("/maze/endCol" )
        self.master.subscribe("/maze/endRow" )
        self.master.subscribe("/maze/blocked" )
        print("Connnect to mqtt-broker")

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)

    def solveMaze(self):
        for step in self.solver.solveMaze():
            step_str = '{},{}'.format(step[0],step[1])
           
            self.publish("/maze/go" , step_str)

if __name__ == '__main__':
    mqttclient=mqtt.Client()
    solverClient = MazeSolverClient(mqttclient)
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("BreadthFirst")
    mqttclient.enable_logger(logger)    
    solverClient.master.loop_forever()
