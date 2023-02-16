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
    update_expression= 'SET {}'.format(','.join(f'#{p}=:{p}' for p in data if p!="email" and p!="company"))
    expression_attribute_values= {f':{p}': v for p,v in data.items() if p!="email" and p!="company"}
    expression_attribute_names= { f'#{p}': p for p in data if p!="email" and p!="company"}


    response= table.update_item(
                Key={
                    'company': event['pathParameters']['company'],
                    'email':data['email']
                    },
                ExpressionAttributeNames = expression_attribute_names,
                ExpressionAttributeValues = expression_attribute_values,
                UpdateExpression = update_expression,
                
                ReturnValues='UPDATED_NEW'
        
         )
    # print(result)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(response["Attributes"])
    }

    return response