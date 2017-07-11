import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import targetGroup as targetGroupApi
import ec2

alb_arn='arn:aws:elasticloadbalancing:us-east-2:811322200214:loadbalancer/app/smith-poc-nodejs-restart-alb/8aea219e2c2c6eb3'
tg_arn='arn:aws:elasticloadbalancing:us-east-2:811322200214:targetgroup/smith-poc-nodejs-restart-tg/7c25fe0e5ca71022'

class TargetGroupTests(unittest.TestCase):

#   def testGetAlbTargetGroups(self):
#     targetGroups = targetGroupApi.getAlbTargetGroups(alb_arn)
#     self.assertGreater(len(targetGroups), 0)
#     for targetGroup in targetGroups:
#       groupArn = targetGroup['TargetGroupArn']
#       print groupArn
#       groupHealth = targetGroupApi.getHealth(groupArn)
#       for targetHealth in groupHealth:
#         print targetHealth
#         self.assertGreater(len(targetHealth), 0)
        
  def testGetHealth(self):
    groupHealth = targetGroupApi.getHealth(tg_arn)
    print 'groupHealth'
    print groupHealth
    for targetHealth in groupHealth:
#       print targetHealth
      self.assertGreater(len(targetHealth), 0)

def main():
  unittest.main()

if __name__ == '__main__':
  main()


