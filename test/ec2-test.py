import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ec2

id='i-047515780d5ff7762'

class ec2Tests(unittest.TestCase):

  def testGetStatus(self):
    targetGroups = targetGroup.getAlbTargetGroups(alb_arn)
    for tg in targetGroups['TargetGroups']:
      
      arn = tg['TargetGroupArn']
      tgHealth = targetGroup.getHealth(arn)

      for tgd in TargetHealthDescriptions:
        

    # self.assertEqual(
    #   ,
    #   'active'
    # )

def main():
  unittest.main()

if __name__ == '__main__':
  main()


