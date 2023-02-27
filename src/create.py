import json
import os
import logging
import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'email' not in data and "company" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the item.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    #to check if the data already exist
    checker =table.query(
        KeyConditionExpression=" #company= :company AND #email= :email",
        ExpressionAttributeValues={":company":data["company"],
        ":email":data["email"]},
        ExpressionAttributeNames={ "#company":"company","#email":"email" }
    )
    if len(checker["Items"])>0:
        return {
            "statusCode":400,
            "body":json.dumps({
                "statusCode":400,
                "message": "The user already exist"
            })
        }
    else:
    
        timestamp=str(time.time())
        item1 = {
            'empid':str(uuid.uuid1()),
            'createdOn':timestamp
        }

        item2={"{}".format(item):data[item] for item in data }
        item1.update(item2)
        # write the todo to the database
        table.put_item(Item=item1)

        # create a response
        response = {
            "statusCode": 201,
            "body": json.dumps({
                "statusCode":201,
                "message":"User created successfully",
                "UserCreated":item1})
        }

        return response