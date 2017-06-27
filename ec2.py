import os
import boto3

client = boto3.client(
    'ec2', 
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

def getStatus(id):
  response = client.describe_instance_status(
    InstanceIds=[
      id
    ]
  )
  details = response
  return response

def reboot(id):
  response = client.reboot_instances(
    InstanceIds=[
      id      
    ]
  )
  return response