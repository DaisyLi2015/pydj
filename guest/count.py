'''
author: daisyli
date: 2017/3/14
description : implement calculate :+ ,-,*,/
'''

class Calculator():
    '''implement +,-,*,/ of two data '''

    def __init__(self,a,b):
        self.a = int(a)
        self.b = int(b)

    # add
    def add(self):
        return self.a+self.b

    # sub
    def sub(self):
        return self.a - self.b

    # mutiply
    def mul(self):
        return self.a * self.b

    #divide
    def div(self):
        return self.a/self.b
