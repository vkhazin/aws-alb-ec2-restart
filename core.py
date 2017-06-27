import os
import boto3

import alb as albApi
import targetGroup as targetGroupApi
import ec2 as ec2Api

def getStatus(albArn):
  albStatus = albApi.getStatus(albArn)

  response = {
    'alb': {
      'status': albStatus
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
        'state': ec2StatusRaw
      }
      targetGroup['targets'].append(ec2Status)

    targetGroups.append(targetGroup)
  
  response['targetGroups'] = targetGroups
  # print response
  return response

