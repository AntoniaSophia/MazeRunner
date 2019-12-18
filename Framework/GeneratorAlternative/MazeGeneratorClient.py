import paho.mqtt.client as mqtt
import time
import array as arr
from maze import *
import sys, getopt
import numpy
import os
import time


if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"


class MazeGeneratorClient:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        #print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None , qos=0, retain=False):
        print("Published message: " , topic , " --> " , message)
        self.master.publish(topic,message,qos,retain)


    def __init__(self):
        # TODO: this is you job now :-)

        print("Constructor MazeGenerator")
        self.startCol = 2
        self.startRow = 2
        self.endCol = 7
        self.endRow = 7
        self.dimensionRow = 27
        self.dimensionCol = 27       
        self.master=mqtt.Client()
        self.master.on_connect=self.onConnect
        self.master.connect(mqtt_server,1883,60)

    def printMaze(self):
        # TODO: this is you job now :-)
        for i in range(len(self.maze)):
            print()
            for j in range(len(self.maze[i])):
                print(self.maze[i][j], end='')


    def sendMaze(self):
        # TODO: this is you job now :-)
        
        self.publish("/maze" , "clear" )
        self.publish("/maze" , "start" )
        self.publish("/maze/dimCol" , self.dimensionCol )
        self.publish("/maze/dimRow" , self.dimensionRow )
        self.publish("/maze/startCol" , self.startCol )
        self.publish("/maze/startRow" , self.startRow )
        self.publish("/maze/endCol" , self.endCol )
        self.publish("/maze/endRow" , self.endRow )

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1): 
                    blocked = ""
                    blocked += str(i)
                    blocked += ","
                    blocked += str(j)
                    self.publish("/maze/blocked" , blocked )

                    if mqtt_server != "127.0.0.1":
                        time.sleep(0.05)
                else:
                    # do nothing because this field is not blocked
                    pass 

        self.publish("/maze" , "end" )        

        #pass

    def loadMaze(self,pathToConfigFile):
        self.maze=numpy.loadtxt(pathToConfigFile, delimiter=',',dtype=int)
        self.dimensionCol=self.maze.shape[0]
        self.dimensionRow=self.maze.shape[1]
        start_arr = numpy.where(self.maze == 2)
        self.startCol=int(start_arr[0][0])
        self.startRow=int(start_arr[1][0])
        end_arr = numpy.where(self.maze == 3)
        self.endCol=int(end_arr[0][0])
        self.endRow=int(end_arr[1][0])

        print(self.startCol,"#",self.startRow)
        print(self.endCol,"#",self.endRow)

    def saveMaze(self,pathToConfigFile):        
        numpy.savetxt(pathToConfigFile, self.mga.getMaze(), fmt="%d", delimiter=",", newline="\n")

    def createNewMaze(self,width, height, complexity, density):
        print(width, height, complexity, density)
        # TODO: this is you job now :-)
        
        self.mga = Maze()
        self.mga.create(int(int(width)/2), int(int(height)/2), Maze.Create.BACKTRACKING) 
        self.maze =  self.mga.getMaze() 
        (x,y)=self.maze.shape
        self.startCol= 1
        self.startRow= 1
        self.endCol= x-2
        self.endRow= y-2
        self.maze[self.startCol,self.startRow] = Maze.ROBOT
        self.maze[self.endCol,self.endRow] = Maze.TARGET
        self.dimensionCol=x
        self.dimensionRow=y    

def main(argv):
    inputfile = ''
    outputfile = ''
    width=7
    height=7
    complexity=50
    density=50

    try:
        opts, args = getopt.getopt(argv,"hi:o:w:h:c:d:",["ifile=","ofile=","width=","height=","complexity=","density="])
    except getopt.GetoptError:
        print ('MazeGeneratorClient.py -i <inputfile> -o <outputfile> -w <width> -h <height> -c <complexity> -d <density>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('MazeGeneratorClient.py -i <inputfile> -o <outputfile> -w <width> -h <height> -c <complexity> -d <density>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-w", "--width"):
            width = arg
        elif opt in ("-h", "--height"):
            height = arg
        elif opt in ("-c", "--complexity"):
            complexity = arg
        elif opt in ("-d", "--density"):
            density = arg                                    
    mg = MazeGeneratorClient()

    if len(inputfile) > 0:
        print ('Input file is ', inputfile)
        mg.loadMaze(inputfile)
    else:
        mg.createNewMaze(width,height,complexity,density)
        if len(outputfile) > 0:
            print ('Output file is ', outputfile)
            mg.saveMaze(outputfile)
    
    mg.printMaze()
    mg.sendMaze()

if __name__ == '__main__':
    main(sys.argv[1:])
