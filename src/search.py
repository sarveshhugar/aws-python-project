import boto3
import json
import logging
import os
# from botocore.exceptions import ClientError

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def search(event,context):
    data=json.loads(event["body"])
    
    #searching using GSI
    if "IndexName" in data:
        if "companytype" not in data:
             logging.error("Search failed")
             raise Exception("Couldn't search for item.")
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="companytype" and p!="sortby" and p!="orderby"))
        Expression_Attribute_Names={ f'#{p}': p for p in data if p!="IndexName" and p!="companytype" and p!="sortby" and p!="orderby"}

        Expression_attribute_values1={":companytype": data["companytype"]}
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="IndexName" and p!="companytype" and p!="sortby" and p!="orderby"}

        Expression_attribute_values1.update(Expression_attribute_values2)

        #if there are non-key attributes also 
        if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
                response=table.query(
                    IndexName=data["IndexName"],
                    KeyConditionExpression="companytype = :companytype",
                    ExpressionAttributeValues = Expression_attribute_values1,
                    FilterExpression = Filter_expression,
                    ExpressionAttributeNames = Expression_Attribute_Names

                    )
        #if there is only gsi index
        else:
                response=table.query(
                IndexName=data["IndexName"],
                KeyConditionExpression="companytype = :companytype",
                ExpressionAttributeValues = Expression_attribute_values1
                )

    #searching using Primary Key
    else:
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="company" and p!="email" and p!="sortby" and p!="orderby"))
        
        #using  sortkey
        if "email" in data:
             Key_Condition_Expression="#company= :company AND #email =:email"
             Expression_attribute_values={":company":data["company"],
                                          ":email":data["email"]}    
        else:
             Key_Condition_Expression="#company= :company"
             Expression_attribute_values={":company":data["company"]}
            
        
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="company" and p!="sortby" and p!="orderby" }
        Expression_Attribute_Names={ f'#{p}': p for p in data if p!="sortby" and p!="orderby"}
        Expression_attribute_values.update(Expression_attribute_values2)

        #if there are non-key attributes also
        if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
            response=table.query(
                KeyConditionExpression = Key_Condition_Expression,
                ExpressionAttributeValues = Expression_attribute_values,
                ExpressionAttributeNames = Expression_Attribute_Names,
                FilterExpression = Filter_expression
            )
        #if there are only key attributes
        else:
            response=table.query(
                KeyConditionExpression = Key_Condition_Expression,
                ExpressionAttributeValues = Expression_attribute_values,
                ExpressionAttributeNames = Expression_Attribute_Names
            )
    
    #if we receive matching items from query
    if len(response["Items"])!=0:   
        if "sortby" in data:
             l,Items=[],response["Items"]
             if not "orderby" in data:
                try:
                    for item in sorted(Items,key = lambda item : item[data["sortby"]]):
                        l.append(item)
                except:
                    logging.error("Invalid attribute")

                else:
                    return {
                    "statusCode":200,
                    "body":json.dumps(l)
                    }
             else:
                try:
                    for item in sorted(Items,key = lambda item : item[data["sortby"]],reverse=True if data["orderby"]=="DESC" else False) :
                        l.append(item)
                except:
                    logging.error("Invalid attribute")

                else:
                    return {
                    "statusCode":200,
                    "body":json.dumps(l)
                    }

        else:
            return {
             "statusCode":200,
             "body":json.dumps(response["Items"])
            }
    
    #if there are no items matched
    else:
         return {
              "statusCode":200,
              "body":"No match found!"
         }
    