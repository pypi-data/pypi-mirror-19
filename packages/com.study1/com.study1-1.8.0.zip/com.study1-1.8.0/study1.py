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
import os


def print_lol2(the_list, needTab=False, level=1, out_file=os.sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
                print_lol2(each_item, needTab, level, out_file);
        else:
            if needTab :
                for tab_stop in range(level):
                    output_line(str(each_item)+"\t", out_file)
                    #print("\t", end="")
            else:       
                output_line(each_item, out_file)


def output_line(each_item, out_file=os.sys.stdout):
    try:
        if out_file != os.sys.stdout :
            with open(out_file, "a") as write_file_item:
                print(each_item, file=write_file_item)
        else:
            print(each_item)
    except IOError as ioErr:
        print("Exception:" + str(ioErr))
