import random


def generator(row_len,column_len):
    list = []
    list2 = []
    for i in range(row_len):
        list2.append(random.randint(0,1))
    for n in range(column_len):
        list.append(list2)
        list2 = []
        for i in range(row_len):
            list2.append(random.randint(0,1))
    print(list)


    

row_len = int(input("how many rows"))
column_len = int(input("how many columns"))
generator(row_len,column_len)

