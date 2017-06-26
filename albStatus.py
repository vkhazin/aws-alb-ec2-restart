import os
import boto3

client = boto3.client(
    'elbv2', 
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

def getAlbStatus(arn):
  response = client.describe_load_balancers(
    LoadBalancerArns=[
        arn,
    ]
  )
  return response

res = getAlbStatus("arn:aws:elasticloadbalancing:us-east-2:811322200214:loadbalancer/app/smith-poc-nodejs-restart-alb/8aea219e2c2c6eb3")

print res

