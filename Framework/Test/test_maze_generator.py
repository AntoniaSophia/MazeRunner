import paho.mqtt.client as mqtt
import time
import array as arr
import paho.mqtt.client as mqtt
import platform
import os

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"
    
if platform.system() != "Windows":
    mqtt_server = "mqtt.eclipse.org"
    
class Sample_Maze_Generator:

    dimensionRow = 5      # X = columns
    dimensionCol = 5      # Y = rows
    startRow = 0
    startCol = 0
    endCol = 4
    endRow = 4

    #########################################################################
    # Definition of maze as rows of zeros and ones (0 = free , 1 = blocked)
    #########################################################################
    # 
    #  Rows (4 rows from 0...3)
    #  |
    #  v
    #  
    #  0   0 0 0 0 0
    #  1   0 1 1 1 1
    #  2   0 1 0 1 0
    #  3   0 1 0 0 0
    #  4   0 0 0 1 0

    #      0 1 2 3 4   <- Columns (5 columns from 0...4)
    #
    #  NOTE:
    #  - Notation for a Field = (row,col)
    #  - (0,0) = is in the upper left corner

    # here: blocked = 
    #  1,1
    #  1,2
    #  1,3
    #  1,4
    #  2,1
    #  2,3
    #  3,1
    #  4,3
    #########################################################################

    #maze = [[0, 0, 0, 0, 0] , [0, 1, 1, 1, 1] , [0, 1, 0, 1, 0] , [0, 1 , 0, 0 , 0] , [0, 0, 0, 1, 0]]
    maze = [[0, 0, 0, 0, 0] , [0, 1, 1, 1, 1] , [0, 1, 0, 1, 0] , [0, 1 , 0, 0 , 0] , [0, 0, 0, 1, 0]]

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        #print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)


    def __init__(self,master):
        print("Constructor Sample_Maze_Generator")
        self.master=master
        self.master.on_connect=self.onConnect
        self.master.connect(mqtt_server,1883,60)


    def sendMaze(self):
        self.publish("/maze" , "clear")
        self.publish("/maze" , "start")
        self.publish("/maze/dimCol" , self.dimensionCol)
        self.publish("/maze/dimRow" , self.dimensionRow)
        self.publish("/maze/startCol" , self.startCol)
        self.publish("/maze/startRow" , self.startRow)
        self.publish("/maze/endCol" , self.endCol)
        self.publish("/maze/endRow" , self.endRow)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1): 
                    blocked = ""
                    blocked += str(i)
                    blocked += ","
                    blocked += str(j)
                    self.publish("/maze/blocked" , blocked)
                else:
                    # do nothing because this field is not blocked
                    pass 

        self.publish("/maze" , "end")


    def loadMaze(self,pathToConfigFile):
        # TODO: this is you job now :-)
        pass
        

    def createNewMaze(self):
        # TODO: this is you job now :-)
        pass


if __name__ == '__main__':
    client=mqtt.Client()

    ##################################
    # Create a sample MQTT Publisher
    ##################################
    aMazePublisher = Sample_Maze_Generator(client)
    aMazePublisher.sendMaze()
    # start the mqtt broker
    client.loop_start()
