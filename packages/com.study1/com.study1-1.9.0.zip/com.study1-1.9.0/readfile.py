'''
Created on Dec 26, 2016

@author: rhan
'''
import os


try:
    the_file = open("test.txt")
    
    print(os.getcwd())
    
    the_file.seek(0)
    man = []
    other = []
    
    for each_line in the_file:
    #     if each_line.find(':') > 0:
        try:
            (role, line_spoken) = each_line.split(":", 1)
            if role == 'Man' :
                man.append(line_spoken.replace(" ", ""))
            elif role == 'Other Man':
                other.append(line_spoken.strip())
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

print("man:", man)
print("other:", other)


try:
    file_out = open("test_out.txt", "a")
    print(other, file=file_out)
    file_out.close()
except IOError :
    print("No found file error.")
finally:
    file_out.close();
    
    

try:
    file_open_test = open("test111.txt")
    file_open_test.readline()
except IOError as err:
    print("No found the file:"+str(err))
finally:
    if 'file_open_test' in locals():
        file_open_test.close()
        
    
        
try:
    with open("test.txt", "r") as file_open_test1, open("test_out.txt", "w") as file_open_test2:
        for each_line in file_open_test1:
            print(each_line.strip(), file=file_open_test2)
except IOError as ioErr:      
    print("Exception:" + str(ioErr))



