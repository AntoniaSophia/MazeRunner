from robotremoteserver import RobotRemoteServer
from examplelibrary import ExampleLibrary

server = RobotRemoteServer(ExampleLibrary(), host='10.0.0.42', port=0,
                           port_file='/tmp/remote-port.txt', serve=False)
server.serve()
