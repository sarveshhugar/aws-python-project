import os
import json

import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    # table = dynamodb.Table('7EDGE-EMPLOYEE')

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'email': event['pathParameters']['email'],
            'company':event['pathParameters']['company']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response