import boto3
import json
import logging
import os


dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def search(event,context):
    data=json.loads(event["body"])
    if "IndexName" not in data:
        logging.error("Search failed")
        raise Exception("Couldn't search for item.")
    
    response=table.query(IndexName=data["IndexName"],
        KeyConditionExpression="gsi1 = :v1",
        ExpressionAttributeValues={
        ":v1": event["pathParameters"]["company"]
        }

        )


    return {
        "statusCode":200,
        "body":json.dumps(response)
    }