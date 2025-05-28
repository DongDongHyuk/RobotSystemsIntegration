from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        m = ['0']*9
        for pk in '123456700':
            p = c([i for i in range(9) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 1:
        pass
    if t == 2:
        pass
    return res

m = randomMap(0)
prt(m,3,3)