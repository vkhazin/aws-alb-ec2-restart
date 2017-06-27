import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import alb as albApi

alb_arn='arn:aws:elasticloadbalancing:us-east-2:811322200214:loadbalancer/app/smith-poc-nodejs-restart-alb/8aea219e2c2c6eb3'

class AblTests(unittest.TestCase):

  def testStatus(self):
    alb = albApi.getStatus(alb_arn)
    print alb
    self.assertIsNotNone(alb)

def main():
  unittest.main()

if __name__ == '__main__':
  main()


