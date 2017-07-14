import boto3

client = boto3.client(
    'ssm'
)

def sendCommand(instanceIds, command):
  response = client.send_command(
      InstanceIds=instanceIds,
      DocumentName='AWS-RunShellScript',
      TimeoutSeconds=60,
      Parameters={
          'commands': [
              command,
          ]
      }
#       OutputS3Region='string',
#       OutputS3BucketName='string',
#       OutputS3KeyPrefix='string',
#       MaxConcurrency='string',
#       MaxErrors='string',
#       ServiceRoleArn='string',
#       NotificationConfig={
#           'NotificationArn': 'string',
#           'NotificationEvents': [
#               'All'|'InProgress'|'Success'|'TimedOut'|'Cancelled'|'Failed',
#           ],
#           'NotificationType': 'Command'|'Invocation'
#       }
  )  
  return response

def restartService(instanceIds, serviceName):
  command = 'sudo service {serviceName} restart'.format(serviceName=serviceName)
  return sendCommand(instanceIds, command)

def killProcessByPortNumber(instanceIds, portNumber):
  command = "sudo kill $(sudo ss -lptn 'sport = :{portNumber}' | grep '(?<=pid=)(\d*)(?=,)' -Po)".format(portNumber=portNumber)
  return sendCommand(instanceIds, command)