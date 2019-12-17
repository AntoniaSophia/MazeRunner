#!/usr/bin/env python

import opc
import time
import numpy
import math
import os
import paho.mqtt.client as mqtt


if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"


class MqttClient:

    def onMessage(self, master, obj, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        print("Received message: ", topic, " --> ", payload)
        if topic == "/maze":
            if payload == "clear":
                self.mazeVisualizer.clearMaze()
            elif payload == "start":
                self.mazeVisualizer.startMaze()
            elif payload == "end":
                self.mazeVisualizer.endMaze()
            else:
                pass
        elif topic == "/maze/startCol":
            if int(payload) < 16:
                self.mazeVisualizer.setStartCol(int(payload))
        elif topic == "/maze/startRow":
            if int(payload) < 16:
                self.mazeVisualizer.setStartRow(int(payload))
        elif topic == "/maze/endCol":
            if int(payload) < 16:
                self.mazeVisualizer.setEndCol(int(payload))
        elif topic == "/maze/endRow":
            if int(payload) < 16:
                self.mazeVisualizer.setEndRow(int(payload))
        elif topic == "/maze/blocked":
            cell = payload.split(",")

            if int(cell[0]) < 16 and int(cell[1]) < 16:
                self.mazeVisualizer.setBlocked(int(cell[1]), int(cell[0]))
        elif topic == "/maze/go":
            cell = payload.split(",")
            col = int(cell[1])
            row = int(cell[0])

            if col < 16 and row < 16:
                if col == self.mazeVisualizer.start_col and row == self.mazeVisualizer.start_row:
                    print("Start")
                elif col == self.mazeVisualizer.end_col and row == self.mazeVisualizer.end_row:
                    print("End")
                else:
                    self.mazeVisualizer.addSolutionStep(col, row)
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
        self.master.subscribe("/maze/go")

        print("Connnect to mqtt-broker")

    def __init__(self, master):
        self.master = master
        self.master.on_connect = self.onConnect
        self.master.on_message = self.onMessage
        self.master.connect(mqtt_server, 1883, 60)
        self.mazeVisualizer = MazeDotMatrix()


class MazeDotMatrix:
    def __init__(self):
        self.numLEDs = 512
        self.columns = 16
        self.rows = 16
        self.client = opc.Client('192.168.17.64:7890')
        self.start_col = -1
        self.start_row = -1
        self.end_col = -1
        self.end_row = -1
        self.clearMaze()

    def getPixelNum(self, col, row):
        pos = 0
        if row < 8:
            if col < 8:
                # 0,0 Segment
                pos = col+(row*8)
            else:
                # 0,1 Segment
                pos = 64+(col-8)+(row*8)
        else:
            if col < 8:
                # 1,0 Segment
                pos = 128+col+(row-8)*8
            else:
                # 1,1 Segement
                pos = 192+(col-8)+(row-8)*8

        # print("{}x{}={}".format(col,row,pos))
        return pos

    def setPixel(self, col, row, color=(0, 0, 0)):
        self.neopixels[self.getPixelNum(col, row)] = color

    def updateMatrix(self):
        self.client.put_pixels(self.neopixels)

    def clearMaze(self):
        self.dot_matrix = [[(0, 0, 0) for x in range(self.columns)]
                           for y in range(self.rows)]
        self.neopixels = [(0, 0, 0)] * self.numLEDs
        self.start_col = -1
        self.start_row = -1
        self.end_col = -1
        self.end_row = -1
        self.updateMatrix()

    def startMaze(self):
        pass

    def endMaze(self):
        pass

    def setBlocked(self, col, row):
        self.setPixel(col, row, color=(100, 0, 0))
        self.updateMatrix()

    def addSolutionStep(self, col, row):
        self.setPixel(col, row, color=(100, 0, 100))
        self.updateMatrix()

    def setStartCol(self, val):
        self.start_col = val

    def setEndCol(self, val):
        self.end_col = val

    def setStartRow(self, val):
        self.start_row = val
        self.setPixel(self.start_col, self.start_row, (100, 100, 0))
        self.updateMatrix()

    def setEndRow(self, val):
        self.end_row = val
        self.setPixel(self.end_col, self.end_row, (0, 100, 100))
        self.updateMatrix()


if __name__ == '__main__':
    mqttclient = mqtt.Client()
    app = MqttClient(mqttclient)
    mqttclient.loop_start()
    while 1:
        time.sleep(1)
