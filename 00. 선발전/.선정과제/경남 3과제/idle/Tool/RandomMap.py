from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        for i in range(2):
            m = ['0']*12
            for pk in '1234567':
                m[c([i for i in range(12) if m[i] == '0'])] = pk
            res.append(''.join(m))
    if t == 1:
        for i in range(2):
            m = ['0']*8
            for pk in '1234567':
                m[c([i for i in range(8) if m[i] == '0'])] = pk
            res.append(''.join(m))
    if t == 2:
        pass
    return res