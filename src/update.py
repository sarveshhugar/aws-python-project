import json
import os
import boto3
import logging
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('7EDGE-EMPLOYEE')

def update(event, context):
    data = json.loads(event['body'])
    # if 'email' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't create the item.")
    

    # update the employee detail in the database
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    result =table.update_item(
        Key={
            'email': event['pathParameters']['id'],
            'company':data['company']
            },
        ExpressionAttributeNames={
            '#val1': 'name'},
        ExpressionAttributeValues={':name': data['name']},
        UpdateExpression='SET #val1 = :name',
        
        ReturnValues='UPDATED_NEW'
        
    )
    print(result)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result["Attributes"])
    }

    return response