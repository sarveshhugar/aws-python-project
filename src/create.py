import json
import os
import logging
import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'email' not in data["item"]:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the item.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    timestamp=str(time.time())
    item1 = {
        'empid':str(uuid.uuid1()),
        'createdOn':timestamp
    }
    item2=data["item"]

    item1.update(item2)
    # write the todo to the database
    table.put_item(Item=item1)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item1)
    }

    return response