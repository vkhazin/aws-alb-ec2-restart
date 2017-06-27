import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core as coreApi

alb_arn='arn:aws:elasticloadbalancing:us-east-2:811322200214:loadbalancer/app/smith-poc-nodejs-restart-alb/8aea219e2c2c6eb3'

class coreTests(unittest.TestCase):

  def testGetStatus(self):
    status = coreApi.getStatus(alb_arn)
    self.assertIsNotNone(status)

  def testReviveInstances(self):
    status = coreApi.getStatus(alb_arn)

    coreApi.reviveInstances(status)
    self.assertIsNotNone(status)

def main():
  unittest.main()

if __name__ == '__main__':
  main()