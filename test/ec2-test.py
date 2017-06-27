import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ec2 as ec2Api

ec2_id='i-0b314f9c31a99621c'

class ec2Tests(unittest.TestCase):

  def testGetDetails(self):
    ec2 = ec2Api.getDetails(ec2_id)
    self.assertIsNotNone(ec2)

  def testGetStatus(self):
    ec2 = ec2Api.getStatus(ec2_id)
    self.assertIsNotNone(ec2)

def main():
  unittest.main()

if __name__ == '__main__':
  main()


