import paho.mqtt.client as mqtt
import time
import array as arr


class MazeSolverClient:

    def __init__(self,master):
        # TODO: this is you job now :-)


        # This MQTT client forwards the requests, so you need a link to the solver
        # --> don't forget to create your algorithm class here, e.g.
        #self.solver = MazeSolverAlgo()
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
        # TODO: this is you job now :-)
        pass


    def onMessage(self, master, obj, msg):
        # TODO: this is you job now :-)
        pass

    def onConnect(self, master, obj, flags, rc):
        # TODO: this is you job now :-)
        pass


    def publish(self, topic, message=None, qos=0, retain=False):
        # TODO: this is you job now :-)
        pass


    def printMaze(self):
        # TODO: this is you job now :-)
        pass


    def loadMaze(self,pathToConfigFile):
        # TODO: this is you job now :-)
        pass
        

    def solveMaze(self):
        # TODO: this is you job now :-)

        # don't forget to publish the results, e.g. 
        self.publish("/maze/go" , step_str)
        pass

    

if __name__ == '__main__':
    mqttclient=mqtt.Client()
    solverClient = MazeSolverClient(mqttclient)
    solverClient.master.loop_forever()
