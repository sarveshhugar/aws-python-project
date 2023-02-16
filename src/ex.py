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
      "company":"hbac"}  
for col in data:
    if col!="company" and col!="email":
        k='#{}'.format(col)
        print(k)
        k='SET #{} = {}'.format(col,data[col])
        print(k)

    
