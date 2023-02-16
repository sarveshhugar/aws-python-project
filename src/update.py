import json
import os
import boto3
import logging
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('7EDGE-EMPLOYEE')

def update(event, context):
    data = json.loads(event['body'])
    if 'email' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the item.")
    



    # update the employee detail in the database
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    for col in data:
        if col!="email" and col!="company":
            table.update_item(
                Key={
                    'company': event['pathParameters']['company'],
                    'email':data['email']
                    },
                ExpressionAttributeNames={
                    '#{}'.format(col): '{}'.format(col)},
                ExpressionAttributeValues={':{}'.format(col): data[col]
                                        },
                UpdateExpression='SET #{} = :{}'.format(col,col),
                
                ReturnValues='UPDATED_NEW'
        
         )
    # print(result)
    # create a response
    response = {
        "statusCode": 200,
        "body": "Update successfull!"
    }

    return response