'''
Created on Dec 24, 2016

@author: rhan
'''

'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
'''

#from com.study1 import print_lol

import study1

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return "x-value:"+str(self.x)+",y-value:"+str(self.y)
    def __add__(self, other):
        p = Point()
        p.x = self.x + other.x
        p.y = self.y + other.y
        return p
    
p1 = Point(3, 4)
p2 = Point(2, 3)

print(p1)
print(p1.y)
print(p1+p2)

movies = ["war", "peace", "gun",[123, 234]]
movies2 = ["war", 1976, "peace", 91, "gun",[123, 234,["1234","qwer"]]]
#com.study1.print_lol(movies)

#study1.print_lol2(movies2, True, 1)

#study1.print_lol2(movies2)
#study1.print_lol2(movies2, True)

study1.print_lol2(movies2, True, 1, "text333.txt")


