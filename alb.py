import os
import boto3

client = boto3.client(
    'elbv2', 
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

def getStatus(arn):
  response = client.describe_load_balancers(
    LoadBalancerArns=[
        arn,
    ]
  )

  lbs = response['LoadBalancers']
  filteredLbs = filter(
    lambda lb: lb['LoadBalancerArn'] == arn, 
    lbs
  )

  lb = iter(filteredLbs).next()
  state = lb

  return state