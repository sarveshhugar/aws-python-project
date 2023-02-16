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
data={"name":"abc",
      "age":"23",
      "email":"ahgdha",
      "company":"hbac",
      "yoe":10,
      "dob":"15th aug"}  
# for col in data:
#     if col!="company" and col!="email":
#         k='#{}'.format(col)
#         print(k)
#         k='SET #{} = {}'.format(col,data[col])
#         print(k)
# update_expression= 'SET {}'.format(','.join(f'#{p}=:{p}' for p in data if p!="email" and p!="company"))
# update_expression= 'SET {}'.format(','.join(f'#{p}=:{p}' for p in data if p!="email" and p!="company"))
# expression_attribute_values= {f':{p}': v for p,v in data.items() if p!="email" and p!="company"}
# expression_attribute_names= { f'#{p}': p for p in data if p!="email" and p!="company"}
# import time
# print(update_expression)
# print(expression_attribute_names)
# print(expression_attribute_values)

    
# print(str(time.ctime(time.time())))
