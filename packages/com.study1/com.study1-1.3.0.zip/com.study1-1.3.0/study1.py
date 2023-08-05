'''
Created on Dec 24, 2016

@author: rhan
'''

'''
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item);
        else:
            print(each_item)

'''

def print_lol2(the_list, needTab=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol2(each_item);
        else:
            if needTab :
                for tab_stop in range(level):
                    print("\t", end="")
            print(each_item)