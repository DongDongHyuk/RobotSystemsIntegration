from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        m = ['x' if i in [1,3,21,23] else '0' for i in range(25)]
        for pk in '123456789a':
            p = c([i for i in [0,5,10,15,20,4,9,14,19,24] if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 1:
        m = ['0']*16
        m[c([9,10,13,14])] = 'x'
        for pk in '12345678':
            p = c([i for i in range(16) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 2:
        fp = c([5,6,9,10])
        di = {5:6,6:5,9:10,10:9}
        for i in range(3):
            m = ['0']*16
            m[di[fp] if i < 2 else fp] = 'x'
            for pk in '12345':
                p = c([i for i in range(16) if m[i] == '0'])
                m[p] = pk
            res.append(''.join(m))
    return res

m1,m2,m3 = randomMap(2)