import os
import boto3

import alb as albApi
import targetGroup as targetGroupApi
import ec2 as ec2Api

def getStatus(albArn):
  albRaw = albApi.getStatus(albArn)

  response = {
    'alb': {
      'arn': albArn,
      'name': albRaw['LoadBalancerName'],
      'dns': albRaw['DNSName'],
      'status': {
        'code': albRaw['State']['Code']
      }
    } 
  }

  targetGroupsRaw = targetGroupApi.getAlbTargetGroups(albArn)
  targetGroups = []
  for targetGroupRaw in targetGroupsRaw:
    tgArn = targetGroupRaw['TargetGroupArn']
    targetGroup = {
      'arn': tgArn,
      'name': targetGroupRaw['TargetGroupName'],
      'targets': []
    }

    targetsRaw = targetGroupApi.getHealth(tgArn)
    for targetRaw in targetsRaw:
      ec2Id = targetRaw['Target']['Id']
      ec2StatusRaw = ec2Api.getStatus(ec2Id)
      ec2Status = {
        'id': ec2Id,
        'targetHealth': {
          'state': targetRaw['TargetHealth']['State'],
          'reason': targetRaw['TargetHealth']['Reason'],
          'description': targetRaw['TargetHealth']['Description']
        },
        'instanceState': {
          'code': ec2StatusRaw['Code'],
          'name': ec2StatusRaw['Name']
        }
      }
      targetGroup['targets'].append(ec2Status)

    targetGroups.append(targetGroup)
  
  response['targetGroups'] = targetGroups
  return response

def reviveInstances(status):
  for targetGroup in status['targetGroups']:
    for target in targetGroup['targets']:
      targetHealth = target['targetHealth']
      targetHealthState = targetHealth['state']
      instanceState = target['instanceState']['name']
      instanceId = target['id']
      # Possible health states:
      # State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining'
      # http://boto3.readthedocs.io/en/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health
      #
      # Possible instance states:
      #  (pending | running | shutting-down | terminated | stopping | stopped )
      # http://boto3.readthedocs.io/en/latest/reference/services/ec2.html?highlight=ec2
      
      if targetHealthState in ('unhealthy','unused'):
        if instanceState == 'running':
          ec2Api.reboot(instanceId)
        elif instanceState == 'stopped':
          ec2Api.start(instanceId)
