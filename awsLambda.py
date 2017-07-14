import json
import os
import boto3
import targetGroup as targetGroupApi
import ssm as ssmApi

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
        .format(AWS_REGION=os.environ['AWS_REGION'], AWS_ACCOUNT_NUMBER=getAccountId(),arnSuffix=arnSuffix)
    targetGroupHealth=targetGroupApi.getHealth(arn)
    # 'State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining'
    unhealtyTargets = [unhealtyTarget for unhealtyTarget in targetGroupHealth if unhealtyTarget['TargetHealth']['State'] in ['unhealthy']]
    targetGroup['UnhealthyTargets'] = unhealtyTargets

    if (len(unhealtyTargets) > 0):
      tags = targetGroupApi.getTags(arn)
      targetGroup['Tags'] = tags
      
  return targetGroups

def restartUnhealthyServices(unhealtyTargetGroups):
  instanceIds = []
  for unhealthyTargetGroup in unhealtyTargetGroups:
    portNumber = None
    for unhealtyTarget in unhealthyTargetGroup['UnhealthyTargets']:
      instanceIds.append(unhealtyTarget['Target']['Id'])
      portNumber = unhealtyTarget['HealthCheckPort']
      
    # Port based approach
    if (len(instanceIds) > 0):
      print 'Restarting unhealty targets: ' + ",".join(instanceIds) + ', port number: ' + portNumber
      ssmApi.killProcessByPortNumber(instanceIds, portNumber)
      
    # Tags based approach      
#     if len(instanceIds) > 0:
#       tags = unhealthyTargetGroup['Tags']
#       filteredTags = [tag for tag in tags if tag['Key'] == 'service-name']
#       if (len(filteredTags) > 0):
#         serviceName = filteredTags[0]['Value']
#         print 'Restarting unhealty targets: ' + ",".join(instanceIds) + ', service name: ' + serviceName
#         ssmApi.restartService(instanceIds, serviceName)
  
def handler(event, context): 
  snsMessages = parseEvent(event)
  unhealthyTargetGroups = findUnhealthyTargetGroups(snsMessages)
  unhealthyTargets = findUnhealthyTargets(unhealthyTargetGroups)
  print unhealthyTargets
  restartUnhealthyServices(unhealthyTargets)
  return unhealthyTargets
  