def parseEvent(event):
  snsMessage = event['Records'][0]['Sns']['Message']
  return snsMessage
