import json

import boto3

s3=boto3.resource('s3')
# bucket=s3.Bucket('myserverlesss3s3bucket-2104')

def createFile(event, context):
    bucket='myserverlesss3s3bucket-2104'
    data = json.loads(event['body'])

    
    
    # create a response
    response = {
        "statusCode": 200,
        "body": event
    }

    return response