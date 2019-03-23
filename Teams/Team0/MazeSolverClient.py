import paho.mqtt.client as mqtt
import time
import array as arr
from MazeSolverAlgo import MazeSolverAlgo

class MazeSolverClient:

    def __init__(self,master):
        # TODO: this is you job now :-)
        self.master=master
        self.master.on_connect=self.onConnect
        self.master.on_message=self.onMessage
        self.master.connect("127.0.0.1",1883,60)

        self.solver = MazeSolverAlgo()
        #pass

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)


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
            self.solver.startMaze(self.solver.columns, self.solver.rows)
        elif topic=="/maze/dimCol":
            self.solver.setDimCols(int(payload))
            self.solver.startMaze(self.solver.columns, self.solver.rows)
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
        self.master.subscribe("/maze")
        self.master.subscribe("/maze/dimRow")
        self.master.subscribe("/maze/dimCol")
        self.master.subscribe("/maze/startCol")
        self.master.subscribe("/maze/startRow")
        self.master.subscribe("/maze/endCol")
        self.master.subscribe("/maze/endRow")
        self.master.subscribe("/maze/blocked")
        print("Connnect to mqtt-broker")

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)


    def printMaze(self):
        # TODO: this is you job now :-)
        self.solver.printMaze()
        #pass


    def loadMaze(self,pathToConfigFile):
        # TODO: this is you job now :-)
        pass
        

    def solveMaze(self):
        # TODO: this is you job now :-)

        for step in self.solver.solveMaze():
            step_str = '{},{}'.format(step[0],step[1])
           
            self.publish("/maze/go" , step_str)

    

if __name__ == '__main__':
    mqttclient=mqtt.Client()
    solverClient = MazeSolverClient(mqttclient)
    solverClient.master.loop_forever()
