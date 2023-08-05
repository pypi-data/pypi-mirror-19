'''
Created on Dec 26, 2016

@author: rhan
'''
import os


try:
    the_file = open("test.txt")
    
    print(os.getcwd())
    
    the_file.seek(0)
    
    for each_line in the_file:
    #     if each_line.find(':') > 0:
        try:
            (role, line_spoken) = each_line.split(":", 1)
            print(line_spoken)
        except ValueError:
            pass
            #print('error:', each_line)
        '''
        if len(the_line) > 0 :
            print(the_line[1], end='')
        '''
    the_file.close()
except IOError:
    print('error:', os.path.exists('text.txt'))
