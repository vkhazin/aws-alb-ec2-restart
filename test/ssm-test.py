import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ssm as ssmApi

ec2_id='i-0b314f9c31a99621c'
serviceName='nodejs-restart'

class ec2Tests(unittest.TestCase):

  def testRestartService(self):
    result = ssmApi.restartService([ec2_id], serviceName)
    print result
    self.assertIsNotNone(result)
    
def main():
  unittest.main()

if __name__ == '__main__':
  main()


