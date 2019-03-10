import unittest
from test import support
from subprocess import Popen, PIPE
import sys, os
import subprocess as sp

pathname = os.path.dirname(sys.argv[0])        
curpath=os.path.abspath(pathname)
broker_path=os.path.join(curpath,"..\MQTTBroker\mosquitto.exe")

class TestMQTTBroker(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("\nStart mosquitto broker")
        assert os.path.isfile(broker_path) == True


        self.p = sp.Popen(broker_path, stdout = sp.PIPE)
        streamdata = self.p.communicate()[0]
        assert self.p.returncode == 1

    def tearDown(self):
        print("\nKill mosquitto broker")
        self.p.kill()
        #streamdata = self.p.communicate()[0]
        assert self.p.returncode == 1

    def test_feature_one(self):
        # Test feature one.
        print("... testing code ...")

    def test_feature_two(self):
        # Test feature two.
        print("... testing code ...")

def test_main():
    support.run_unittest(TestMQTTBroker)

if __name__ == '__main__':
    test_main()