#coding=utf-8
import math
import random
class hex10to36():
    def create():
        loop = '0123456789abcdefghijklmnopqrstuvwxyz'
#n = 1409980009869
        n = int(math.floor(2147483648*random.random()))
        a = []
        while n != 0:
            a.append(loop[n%36])
            n = n/36
            a.reverse()
        out = ''.join(a)
        return out
