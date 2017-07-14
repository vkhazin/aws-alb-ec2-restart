import boto3
import requests

client = boto3.client(
    'ec2'
)

def getDetails(id):
  response = client.describe_instances(
    InstanceIds=[
      id
    ]
  )
  reservations = response['Reservations']
  instances = iter(reservations).next()['Instances']
  instance = iter(instances).next()
  return instance

def getStatus(id):
  response = client.describe_instance_status(
    InstanceIds=[
      id
    ],
    IncludeAllInstances=True
  )
  statuses = response['InstanceStatuses']
  status = iter(statuses).next()
  state = status['InstanceState']
  return state

def reboot(id):
  print('Rebooting instance: ' + id)
  response = client.reboot_instances(
    InstanceIds=[
      id      
    ]
  )
  return response

def start(id):
  print('Starting instance: ' + id)
  response = client.start_instances(
    InstanceIds=[
      id      
    ]
  )
  return response

def getInstanceId():
  response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
  instanceId = response.text
  return instanceId
  