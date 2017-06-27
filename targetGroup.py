import os
import boto3

client = boto3.client(
    'elbv2', 
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

def getAlbTargetGroups(albArn):
  response = client.describe_target_groups(
    LoadBalancerArn=albArn
  )
  targetGroups = response['TargetGroups']
  return targetGroups

def getHealth(groupArn):
  response = client.describe_target_health(
    TargetGroupArn=groupArn
  )


  for tgd in response['TargetHealthDescriptions']:
    targetHealth = tgd['TargetHealth']
    state = targetHealth['State']
    # 'State': 'initial'|'healthy'|'unhealthy'|'unused'|'draining',
    # if state == 'unused':

  return response['TargetHealthDescriptions']