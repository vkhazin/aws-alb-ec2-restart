import json
import os
import boto3
import targetGroup as targetGroupApi
import ssm as ssmApi
import cloudWatch as cloudWatchApi

alarmNamesPrefix='awsapplicationelb-'

client = boto3.client(
    'sts'
)
accountId = None

def getAccountId():
  global accountId
  if accountId is None:
    print 'Getting AccountId using Aws Api'
    accountId = client.get_caller_identity()["Account"]
  return accountId

def parseEvent(event):
  return map(lambda record: json.loads(record['Sns']['Message']), event['Records'])

def parseSnsMessages(snsMessages):
  for snsMessage in snsMessages:
    alarmName = snsMessage['AlarmName']
    unhealthyTargetGroups = []
    dimensions = snsMessage['Trigger']['Dimensions']
    targetGroups = [dimension for dimension in dimensions if dimension['name'] == 'TargetGroup']
    unhealthyTargetGroups.extend(targetGroups)
    yield {
      'AlarmName': alarmName,
      'TargetGroups': unhealthyTargetGroups
    }
#   return unhealthyTargetGroups

def findUnhealthyTargets(targetGroups):
# [{u'name': u'TargetGroup', u'value': u'targetgroup/smith-poc-nodejs-restart-tg/7c25fe0e5ca71022'}]
  for targetGroup in targetGroups:
    arnSuffix = targetGroup['value']
    arn='arn:aws:elasticloadbalancing:{AWS_REGION}:{AWS_ACCOUNT_NUMBER}:{arnSuffix}' \
        .format(AWS_REGION=os.environ['AWS_REGION'], AWS_ACCOUNT_NUMBER=getAccountId(),arnSuffix=arnSuffix)
    targetGroupHealth=targetGroupApi.getHealth(arn)
    # 'State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining'
    unhealthyTargets = [unhealthyTarget for unhealthyTarget in targetGroupHealth if unhealthyTarget['TargetHealth']['State'] in ['unhealthy']]
    targetGroup['UnhealthyTargets'] = unhealthyTargets
    
    # No more in use
#     if (len(unhealthyTargets) > 0):
#       tags = targetGroupApi.getTags(arn)
#       targetGroup['Tags'] = tags
      
  return targetGroups

def restartUnhealthyServices(unhealthyTargetGroups):
  instanceIds = []
  for unhealthyTargetGroup in unhealthyTargetGroups:
    portNumber = None
    for unhealthyTarget in unhealthyTargetGroup['UnhealthyTargets']:
      instanceIds.append(unhealthyTarget['Target']['Id'])
      portNumber = unhealthyTarget['HealthCheckPort']
      
    # Port based approach
    if (len(instanceIds) > 0):
      print 'Restarting unhealthy targets: ' + ",".join(instanceIds) + ', port number: ' + portNumber
      ssmApi.killProcessByPortNumber(instanceIds, portNumber)
    else:
      raise ValueError('Could not find any unhealthy targets to restart!')
    # Tags based approach      
#     if len(instanceIds) > 0:
#       tags = unhealthyTargetGroup['Tags']
#       filteredTags = [tag for tag in tags if tag['Key'] == 'service-name']
#       if (len(filteredTags) > 0):
#         serviceName = filteredTags[0]['Value']
#         print 'Restarting unhealthy targets: ' + ",".join(instanceIds) + ', service name: ' + serviceName
#         ssmApi.restartService(instanceIds, serviceName)
  
def handler(event, context): 
  snsMessages = parseEvent(event)
  for targetHealthGroup in parseSnsMessages(snsMessages):
    unhealthyTargets = findUnhealthyTargets(targetHealthGroup['TargetGroups'])
    print(json.dumps(unhealthyTargets))
    restartUnhealthyServices(unhealthyTargets)
    alarmName = targetHealthGroup['AlarmName'].replace(alarmNamesPrefix, '')
    print('Resetting alarm: {alarmName}'.format(alarmName=alarmName))
    cloudWatchApi.resetAlarmState(alarmName=alarmName)
  return unhealthyTargets
  