import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import targetGroup
import ec2

alb_arn='arn:aws:elasticloadbalancing:us-east-2:811322200214:loadbalancer/app/smith-poc-nodejs-restart-alb/8aea219e2c2c6eb3'

class TargetGroupTests(unittest.TestCase):

  def testGetAlbTargetGroups(self):
    targetGroups = targetGroup.getAlbTargetGroups(alb_arn)
    print targetGroups
    # for tg in targetGroups['TargetGroups']:
      
    #   arn = tg['TargetGroupArn']
    #   tgHealthDescs = targetGroup.getHealth(arn)

    #   self.assertGreater(len(tgHealthDescs), 0)
      # for tgd in tgHealthDescs:
      #   targetHealth = tgd['TargetHealth']
      #   state = targetHealth['State']
        # 'State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining',
        # if state == 'unused':

def main():
  unittest.main()

if __name__ == '__main__':
  main()


