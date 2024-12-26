my_dict = {"penis": 10, "vagina": 11}

#print (my_dict.keys()[my_dict.values().index([10])])
print(my_dict.values())
print(type(list(my_dict.values())))
print(list(my_dict.values()).index(10))
print(list(my_dict.keys())[list(my_dict.values()).index(10)])

