import json
import os

import boto3
dynamodb = boto3.resource('dynamodb')

table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])
def list(event, context):
    
    # fetch all employees names from the database
    result = table.query(
        
        KeyConditionExpression='company= :company',
        ExpressionAttributeValues={
        ':company':event['pathParameters']['company'] 
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response