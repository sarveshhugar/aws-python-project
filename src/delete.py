import boto3
import os
import json
dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


    # delete the employee detail from the database
    response=table.delete_item(
        Key={
            'company': event['pathParameters']['company'],
            'email': event['pathParameters']['email']
            
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": "Deleted."
    }

    return response