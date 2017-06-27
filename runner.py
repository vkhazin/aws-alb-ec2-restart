import sys
import core

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'Missing Application Load Balancer arn, pass it as a first parameter'
    exit
  else:
    arn = sys.argv[1]
    print 'Checking status for: ' + arn
    status = core.getStatus(arn)
    core.reviveInstances(status)