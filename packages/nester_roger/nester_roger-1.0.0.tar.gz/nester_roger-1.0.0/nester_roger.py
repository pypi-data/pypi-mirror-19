'''
this py can print each nest list in mylist
'''
def print_lol(mylist):
    '''this function can print each item in mylist'''
    for each in mylist:
        if isinstance(each,list):
            print_lol(each)
        else:
            print(each)



