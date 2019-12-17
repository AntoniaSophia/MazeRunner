import sys
from subprocess import Popen
import os
import threading
import time
import platform
import paho.mqtt.client as paho

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory,"..","..")
os.environ['FOR_IGNORE_EXCEPTIONS'] = '1'
pythonVar = "python"


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"

class Control:
    def __init__(self):
        self.mqtt_broker_proc = 0
        self.maze_gui_proc = 0
        self.team = ""
        self.generator_action = 0
        self.running = 1
        self.mqtt_broker_state = 0
        self.maze_gui_state = 0
        self.solver_action_proc = 0
        self.solver_action_state = 0

        threading.Thread(target=self.monitor).start()

    def checkproc(self,p):
        state = 0
        if p != 0:
            poll = p.poll()

            if poll == None:
                state = 1
            else:
                state = -1
        return state


    def monitor(self):
        while self.running:
            self.mqtt_broker_state = self.checkproc(self.mqtt_broker_proc)
            self.maze_gui_state = self.checkproc(self.maze_gui_proc)
            self.solver_action_state = self.checkproc(self.solver_action_proc)

            # print("Monitor: {} {} {}".format(self.mqtt_broker_state, self.maze_gui_state, self.solver_action_state))
            
            time.sleep(1)
         

control = Control()

def handler(a,b=None):
    control.running=0
    sys.exit(0)

def install_handler():
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(handler, True)

install_handler()

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()

def maze_visualize():
    print('Maze Visualizer started')
    
    sys.stdout.flush()

    executeSript=os.path.join(projectDirectory,"Framework","Visualizer","maze_visualize.py")
    control.maze_gui_proc = Popen([pythonVar,executeSript],shell=False) # something long running


def maze_solver_loader():

    if control.team == "":
        print("Load Team please!")
    else:
        print('Solver Action')
        executeSript=os.path.join(projectDirectory,"Teams",control.team,"MazeSolverClient.py")
        control.solver_action_proc = Popen([pythonVar,executeSript],shell=True,stdout=sys.stdout,stderr=sys.stderr) # something long running

def maze_solver_action():
    print('Solve Maze!')
    
    client= paho.Client("maze_control")

    client.connect(host=mqtt_server)

    client.publish("/maze","solve")

def mqtt_broker():
    print('MQTT Broker started')
    sys.stdout.flush()
    if sys.platform == "win32":
        executeSript=os.path.join(projectDirectory,"Framework","MQTTBroker","mosquitto.exe")
        control.mqtt_broker_proc = Popen([executeSript],shell=False) # something long running
   

def load_team(team):
    print('Load {}'.format(team))
    control.team=team

def generator_action(width,height,complexity,density):
    print("w: {} | h: {} | c: {} | d: {}".format(width, height, complexity, density))
    
    print('Generator Action')
    executeSript=os.path.join(projectDirectory,"Framework","Generator","MazeGeneratorClient.py")
    print(['python',executeSript,'-w', width,'-h',height,'-c',complexity,'-d',density])
    control.generator_action = Popen(['python',executeSript,"--width="+str(width),"--height="+str(height),"--complexity="+str(complexity),"--density="+str(density)],shell=False) # something long running

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
    control.mqtt_broker_proc.terminate()    

if __name__ == '__main__':
    import maze_control
    maze_control.vp_start_gui()




