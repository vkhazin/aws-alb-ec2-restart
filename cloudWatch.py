import boto3

client = boto3.client(
    'cloudwatch'
)

def resetAlarmState(alarmName):
  response = client.set_alarm_state(
      AlarmName=alarmName,
      StateValue='OK',
      StateReason='Manual Reset to OK state'
  ) 
  return response

def getAlarmState(alarmName):
  response = client.describe_alarms(
      AlarmNames=[
          alarmName,
      ]
  )
  return response['MetricAlarms'][0]['StateValue']

