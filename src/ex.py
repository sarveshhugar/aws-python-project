# import uuid
# print(type(str(uuid.uuid1())))
# d={
#     "a":10,
#     "b":11
# }
# k={"c":12
#      }
# # l= {'email': data['email'],
# #         'name':data['name'] ,
# #         'YOE':data['YOE'],
# #         'company':data['company']}
# k.update(d)
# print(k)
# l=[  ]
k=''
data={"gsi1":"7EDGE",
    # "from":"bangalore",
    #   "YOE":"5",
    #   "yearjoined":"2004",
      "IndexName":"gsi1-index"
      }  
# for col in data:
#     if col!="company" and col!="email":
#         k='#{}'.format(col)
#         print(k)
#         k='SET #{} = {}'.format(col,data[col])
#         print(k)
# update_expression= 'SET {}'.format(','.join(f'#{p}=:{p}' for p in data if p!="email" and p!="company"))
# update_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="email" and p!="company"))
# expression_attribute_values= {f':{p}': v for p,v in data.items() if p!="email" and p!="company"}
# expression_attribute_names= { f'#{p}': p for p in data if p!="email" and p!="company"}
# import time
# print(update_expression)
# print(expression_attribute_names)
# print(expression_attribute_values)
# Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="gsi1" and p!="company" and p!="email"))
# Expression_Attribute_Names={ f'#{p}': p for p in data if p!="email" and p!="company" and p!="gsi1" }

# Expression_attribute_values1={":gsi1": data["gsi1"]}
# Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="email" and p!="company" and p!="gsi1"}
# Expression_attribute_values1.update(Expression_attribute_values2)
Filter_expression= '{}'.format(' AND '.join(f'#{p}=:{p}' for p in data if p!="IndexName" and p!="IndexName" and p!="gsi1" and p!="company" and p!="email"))
Expression_Attribute_Names={ f'#{p}': p for p in data if p!="IndexName" and p!="email" and p!="company" and p!="gsi1" }

Expression_attribute_values1={":gsi1": data["gsi1"]}
Expression_attribute_values2= { f':{p}': data[p] for p in data if p!="IndexName" and p!="email" and p!="company" and p!="gsi1"}

Expression_attribute_values1.update(Expression_attribute_values2)
    

# print(str(time.ctime(time.time())))
print(Expression_attribute_values1)
print(Filter_expression)
print(Expression_Attribute_Names)
