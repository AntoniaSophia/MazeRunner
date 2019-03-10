import unittest
from test import support
from subprocess import Popen, PIPE
import sys, os


pathname = os.path.dirname(sys.argv[0])        
curpath=os.path.abspath(pathname)

print('full path =',curpath )       

class MyTestCase1(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        broker_path=os.path.join(curpath,"..\MQTTBroker\mosquitto.exe")
        print(broker_path)
        self.p = Popen(broker_path, shell=True, stdout = PIPE)

    def tearDown(self):
        print("... code to execute to clean up after tests ...")

    def test_feature_one(self):
        # Test feature one.
       print("... testing code ...")

    def test_feature_two(self):
        # Test feature two.
        print("... testing code ...")

def test_main():
    support.run_unittest(MyTestCase1)

if __name__ == '__main__':
    test_main()