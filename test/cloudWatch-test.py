import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cloudWatch as cloudWatchApi

alarmName='smith-poc-nodejs-alarm-unhealthy-hosts'

class ec2Tests(unittest.TestCase):

  def testResetAlarm(self):
    result = cloudWatchApi.resetAlarmState(alarmName)
    self.assertIsNotNone(result)

  def testGetAlarm(self):
    result = cloudWatchApi.resetAlarmState(alarmName)
    alarmState = cloudWatchApi.getAlarmState(alarmName)
    self.assertEqual(alarmState.upper(), 'OK')
    
def main():
  unittest.main()

if __name__ == '__main__':
  main()


