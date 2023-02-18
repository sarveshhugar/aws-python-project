import boto3
import json
import logging
import os


dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def search(event,context):
    data=json.loads(event["body"])
    
    if "IndexName" in data:
        if "IndexName" not in data and "companytype" not in data:
             logging.error("Search failed")
             raise Exception("Couldn't search for item.")
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="companytype"))
        Expression_Attribute_Names={ f'#{p}': p for p in data if p!="IndexName" and p!="companytype" }

        Expression_attribute_values1={":companytype": data["companytype"]}
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="IndexName" and p!="companytype"}

        Expression_attribute_values1.update(Expression_attribute_values2)

        if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
                response=table.query(
                    IndexName=data["IndexName"],
                    KeyConditionExpression="companytype = :companytype",
                    ExpressionAttributeValues = Expression_attribute_values1,
                    FilterExpression = Filter_expression,
                    ExpressionAttributeNames = Expression_Attribute_Names

                    )
        else:
                response=table.query(
                IndexName=data["IndexName"],
                KeyConditionExpression="companytype = :companytype",
                ExpressionAttributeValues = Expression_attribute_values1
                )

    else:
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="company" and p!="email"))
        
        if "email" in data:
             Key_Condition_Expression="#company= :company AND #email =:email"
             Expression_attribute_values={":company":data["company"],
                                          ":email":data["email"]}
            
        else:
             Key_Condition_Expression="#company= :company"
             Expression_attribute_values={":company":data["company"]}
            
        
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="company" }
        Expression_Attribute_Names={ f'#{p}': p for p in data }
        Expression_attribute_values.update(Expression_attribute_values2)

        if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
            response=table.query(
                KeyConditionExpression = Key_Condition_Expression,
                ExpressionAttributeValues = Expression_attribute_values,
                ExpressionAttributeNames = Expression_Attribute_Names,
                FilterExpression = Filter_expression
            )
        else:
            response=table.query(
                KeyConditionExpression = Key_Condition_Expression,
                ExpressionAttributeValues = Expression_attribute_values,
                ExpressionAttributeNames = Expression_Attribute_Names
            )
    
    
    if len(response["Items"])!=0:    
        return {
            "statusCode":200,
            "body":json.dumps(response["Items"])
        }
    else:
         return {
              "statusCode":200,
              "body":"No match found!"
         }
    