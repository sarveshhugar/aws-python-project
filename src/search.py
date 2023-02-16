import boto3
import json
import logging
import os


dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def search(event,context):
    data=json.loads(event["body"])
    if "email" not in data and "company" not in data:
        logging.error("Creation failed")
        raise Exception("Couldn't search for item.")
    
    response=table.query(
        KeyConditionExpression={
        "company":data["company"],
        "email":data["email"]
            }
        )


    return {
        "statusCode":200,
        "body":json.dumps(response)
    }