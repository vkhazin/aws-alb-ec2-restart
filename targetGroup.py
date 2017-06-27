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
  return response['TargetHealthDescriptions']