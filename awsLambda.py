import json
import targetGroup as targetGroupApi
import os

def parseEvent(event):
  return map(lambda record: json.loads(record['Sns']['Message']), event['Records'])

def findUnhealthyTargetGroups(snsMessages):
  unhealtyTargetGroups = []
  for snsMessage in snsMessages:
    dimensions = snsMessage['Trigger']['Dimensions']
    targetGroups = [dimension for dimension in dimensions if dimension['name'] == 'TargetGroup']
    unhealtyTargetGroups.extend(targetGroups)
  return unhealtyTargetGroups

def findUnhealthyTargets(targetGroups):
# [{u'name': u'TargetGroup', u'value': u'targetgroup/smith-poc-nodejs-restart-tg/7c25fe0e5ca71022'}]
  for targetGroup in targetGroups:
    arnSuffix = targetGroup['value']
    arn='arn:aws:elasticloadbalancing:{AWS_REGION}:{AWS_ACCOUNT_NUMBER}:{arnSuffix}' \
        .format(AWS_REGION=os.environ['AWS_REGION'], AWS_ACCOUNT_NUMBER=os.environ['AWS_ACCOUNT_NUMBER'],arnSuffix=arnSuffix)
    targetGroupHealth=targetGroupApi.getHealth(arn)
    # 'State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining'
    unhealtyTargets = [unhealtyTarget for unhealtyTarget in targetGroupHealth if unhealtyTarget['TargetHealth']['State'] in ['unused', 'unhealthy']]
    targetGroup['UnhealthyTargets'] = unhealtyTargets

  return targetGroups

def lambda_handler(event, context): 
  snsMessages = parseEvent(event)
  unhealthyTargetGroups = findUnhealthyTargetGroups(snsMessages)
  unhealthyTargets = findUnhealthyTargets(unhealthyTargetGroups)
  print unhealthyTargets
  return unhealthyTargets
  