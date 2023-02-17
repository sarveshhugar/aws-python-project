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
    
    Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="gsi1" and p!="company" and p!="email"))
    Expression_Attribute_Names={ f'#{p}': p for p in data if p!="IndexName" and p!="email" and p!="company" and p!="gsi1" }

    Expression_attribute_values1={":gsi1": data["gsi1"]}
    Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="IndexName" and p!="email" and p!="company" and p!="gsi1"}

    Expression_attribute_values1.update(Expression_attribute_values2)

    if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
             response=table.query(
                IndexName=data["IndexName"],
                KeyConditionExpression="gsi1 = :gsi1",
                ExpressionAttributeValues = Expression_attribute_values1,
                FilterExpression = Filter_expression,
                ExpressionAttributeNames = Expression_Attribute_Names

                )
    else:
            response=table.query(
                IndexName=data["IndexName"],
                KeyConditionExpression="gsi1 = :gsi1",
                ExpressionAttributeValues = Expression_attribute_values1
                )

        
    return {
        "statusCode":200,
        "body":json.dumps(response["Items"])
    }