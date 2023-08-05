def Print(datas):#a function print every element in a list
    for data in datas:
        if isinstance(data,list):
            Print(data)
        else:
            print(data)
