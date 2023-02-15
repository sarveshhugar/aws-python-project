import json
import os

import boto3
dynamodb = boto3.client('dynamodb')


def list(event, context):
    # table = dynamodb.Table('7EDGE-EMPLOYEE')
    # table = dynamodb.Table()


    # fetch all employees names from the database
    result = dynamodb.query(
        TableName=os.environ['DYNAMODB_TABLE'],
        KeyConditionExpression='company= :company',
        ExpressionAttributeValues={
        ':company': {'S' : event['pathParameters']['company'] }
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response