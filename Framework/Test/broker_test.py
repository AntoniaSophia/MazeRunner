import unittest
from test import support
from subprocess import Popen, PIPE
import sys, os
#http://www.bx.psu.edu/~nate/pexpect/pexpect.html
from pexpect import popen_spawn
from test_mqtt_client import SubTestDemo, SubTest, PubTest, PubTestDemo
import time

pathname = os.path.dirname(sys.argv[0])        
curpath=os.path.abspath(pathname)
broker_path=os.path.join(curpath,"..\MQTTBroker\mosquitto.exe")

class TestMQTTBroker(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("\nStart mosquitto broker")
        assert os.path.isfile(broker_path) == True
        self.c = popen_spawn.PopenSpawn(broker_path)

    def tearDown(self):
        print("\nKill mosquitto broker")
        self.c.kill(9)

    def test_feature_one(self):
        # Test feature one.
        print("... testing code ...")
        self.testerPub = PubTestDemo()
        self.testerSub = SubTestDemo("/maze")
        time.sleep(1)
        self.testerPub.sendMessage("/maze","Hallo123")
        time.sleep(1)
        print("Message:"+self.testerSub.getlastmessage())
        self.assertEqual(self.testerSub.getlastmessage(),'Hallo123')


    def test_feature_two(self):
        # Test feature two.
        print("... testing code ...")

def test_main():
    support.run_unittest(TestMQTTBroker)

if __name__ == '__main__':
    test_main()