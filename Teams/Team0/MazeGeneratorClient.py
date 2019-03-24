import paho.mqtt.client as mqtt
import time
import array as arr
from maze_generator_algo_2 import MazeGeneratorAlgo
import sys, getopt
import numpy

class MazeGeneratorClient:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        #print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
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
        self.master.connect("127.0.0.1",1883,60)

        self.mga = MazeGeneratorAlgo(self.dimensionRow,self.dimensionCol,self.startCol,self.startRow,self.endCol,self.endRow)
        self.mga.createMaze()
        self.maze=self.mga.getMaze()

        #pass


    def printMaze(self):
        # TODO: this is you job now :-)
        for i in range(len(self.maze)):
            print()
            for j in range(len(self.maze[i])):
                print(self.maze[i][j], end='')

        #pass

    def sendMaze(self):
        # TODO: this is you job now :-)
        
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

    def createNewMaze(self):
        # TODO: this is you job now :-)
        self.mga = MazeGeneratorAlgo(self.dimensionRow,self.dimensionCol,self.startCol,self.startRow,self.endCol,self.endRow)
        self.mga.createMaze()
        self.startCol= self.mga.robotStart_col
        self.startRow= self.mga.robotStart_row
        self.endCol= self.mga.targetPos_col
        self.endRow= self.mga.targetPos_row
        self.maze=self.mga.getMaze()
        
        #pass

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    mg = MazeGeneratorClient()

    if len(inputfile) > 0:
        print ('Input file is ', inputfile)
        mg.loadMaze(inputfile)
    else:
        mg.createNewMaze()
        if len(outputfile) > 0:
            print ('Output file is ', outputfile)
            mg.saveMaze(outputfile)
    mg.printMaze()
    mg.sendMaze()

if __name__ == '__main__':
    main(sys.argv[1:])
