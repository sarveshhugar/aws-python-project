import boto3
import json
import logging
import os
# from botocore.exceptions import ClientError

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def search(event,context):
    data=json.loads(event["body"])
    
    ignoreExp={"sortby","orderby","limit","lastkey"}

    #searching using GSI
    if "IndexName" in data:
        if "companytype" not in data:
             logging.error("Search failed")
             raise Exception("Couldn't search for item.")
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="companytype" and p not in ignoreExp))
        Expression_Attribute_Names={ f'#{p}': p for p in data if p!="IndexName" and p!="companytype" and p not in ignoreExp}

        Expression_attribute_values1={":companytype": data["companytype"]}
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="IndexName" and p!="companytype" and p not in ignoreExp}

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
    #-------------------------------------------------------------------------------------------------------------
    #search,filter and sort using Primary Key
    else:
        Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="company" and p!="email" and p not in ignoreExp))
        
        #using  sortkey
        if "email" in data:
             Key_Condition_Expression="#company= :company AND #email =:email"
             Expression_attribute_values={":company":data["company"],
                                          ":email":data["email"]}    
        else:
             Key_Condition_Expression="#company= :company"
             Expression_attribute_values={":company":data["company"]}
            
        
        Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="company" and p not in ignoreExp }
        Expression_Attribute_Names={ f'#{p}': p for p in data if p not in ignoreExp}
        Expression_attribute_values.update(Expression_attribute_values2)

        #if there are non-key attributes also
        if len(Filter_expression)!=0 and len(Expression_Attribute_Names)!=0:
            if "sortby" in data:
                #if there is orderby
                if "orderby" in data:
                    if "lastkey" in data:
                        response=table.query(
                            IndexName="{}-index".format(data["sortby"]),
                            KeyConditionExpression = Key_Condition_Expression,
                            ExpressionAttributeValues = Expression_attribute_values,
                            ExpressionAttributeNames = Expression_Attribute_Names,
                            FilterExpression = Filter_expression,
                            ScanIndexForward = False if data["orderby"]=="desc" else True ,
                            Limit = 10 if not "limit" in data else data["limit"],
                            ExclusiveStartKey= data["lastkey"]   
                        )
                    else:
                        response=table.query(
                            IndexName="{}-index".format(data["sortby"]),
                            KeyConditionExpression = Key_Condition_Expression,
                            ExpressionAttributeValues = Expression_attribute_values,
                            ExpressionAttributeNames = Expression_Attribute_Names,
                            FilterExpression = Filter_expression,
                            ScanIndexForward = False if data["orderby"]=="desc" else True ,
                            Limit = 10 if not "limit" in data else data["limit"]    
                        )
                else:
                    if "lastkey" in data:
                        response=table.query(
                            IndexName="{}-index".format(data["sortby"]),
                            KeyConditionExpression = Key_Condition_Expression,
                            ExpressionAttributeValues = Expression_attribute_values,
                            ExpressionAttributeNames = Expression_Attribute_Names,
                            FilterExpression = Filter_expression,
                            ScanIndexForward = True ,
                            Limit = 10 if not "limit" in data else data["limit"],
                            ExclusiveStartKey = data["lastkey"]  
                        )
                    else:
                        response=table.query(
                        IndexName="{}-index".format(data["sortby"]),
                        KeyConditionExpression = Key_Condition_Expression,
                        ExpressionAttributeValues = Expression_attribute_values,
                        ExpressionAttributeNames = Expression_Attribute_Names,
                        FilterExpression = Filter_expression,
                        ScanIndexForward = True ,
                        Limit = 10 if not "limit" in data else data["limit"]  
                    )
            else:
                #if nothing to sort just filter and give search results
                if "lastkey" in data:
                    response=table.query(
                        KeyConditionExpression = Key_Condition_Expression,
                        ExpressionAttributeValues = Expression_attribute_values,
                        ExpressionAttributeNames = Expression_Attribute_Names,
                        FilterExpression = Filter_expression,
                        Limit = 10 if not "limit" in data else data["limit"],
                        ExclusiveStartKey = data["lastkey"] 
                    )
                else:
                    response=table.query(
                    KeyConditionExpression = Key_Condition_Expression,
                    ExpressionAttributeValues = Expression_attribute_values,
                    ExpressionAttributeNames = Expression_Attribute_Names,
                    FilterExpression = Filter_expression,
                    Limit = 10 if not "limit" in data else data["limit"] 
                )

        #if there is only partition key attribute
        else:
            if "sortby" in data:
                if "orderby" in data:
                    if "lastkey" in data:  
                        response=table.query(
                            IndexName= '{}-index'.format(data["sortby"]),
                            KeyConditionExpression = Key_Condition_Expression,
                            ExpressionAttributeValues = Expression_attribute_values,
                            ExpressionAttributeNames = Expression_Attribute_Names,
                            ScanIndexForward= False if data["orderby"]=="desc" else True,
                            Limit = 10 if not "limit" in data else data["limit"],
                            ExclusiveStartKey= data["lastkey"] 
                        )
                    else:
                            response=table.query(
                            IndexName= '{}-index'.format(data["sortby"]),
                            KeyConditionExpression = Key_Condition_Expression,
                            ExpressionAttributeValues = Expression_attribute_values,
                            ExpressionAttributeNames = Expression_Attribute_Names,
                            ScanIndexForward= False if data["orderby"]=="desc" else True,
                            Limit = 10 if not "limit" in data else data["limit"] 
                        )
                else:
                    if "lastkey" in data:
                        response=table.query(
                        IndexName= '{}-index'.format(data["sortby"]),
                        KeyConditionExpression = Key_Condition_Expression,
                        ExpressionAttributeValues = Expression_attribute_values,
                        ExpressionAttributeNames = Expression_Attribute_Names,
                        ScanIndexForward= True,
                        Limit = 10 if not "limit" in data else data["limit"],
                        ExclusiveStartKey= data["lastkey"] 
                        )
                    else:
                        response=table.query(
                        IndexName= '{}-index'.format(data["sortby"]),
                        KeyConditionExpression = Key_Condition_Expression,
                        ExpressionAttributeValues = Expression_attribute_values,
                        ExpressionAttributeNames = Expression_Attribute_Names,
                        ScanIndexForward= True,
                        Limit = 10 if not "limit" in data else data["limit"] 
                        )

            else:
                if "lastkey" in data:
                    response=table.query(
                        KeyConditionExpression = Key_Condition_Expression,
                        ExpressionAttributeValues = Expression_attribute_values,
                        ExpressionAttributeNames = Expression_Attribute_Names,
                        Limit = 10 if not "limit" in data else data["limit"],
                        ExclusiveStartKey = data["lastkey"] 
                    )
                else:
                    response=table.query(
                    KeyConditionExpression = Key_Condition_Expression,
                    ExpressionAttributeValues = Expression_attribute_values,
                    ExpressionAttributeNames = Expression_Attribute_Names,
                    Limit = 10 if not "limit" in data else data["limit"] 
                )
    
    return {
             "statusCode":200,
             "body":json.dumps(response["Items"]) if len(response["Items"])!=0 else "no match found !"
            }
    