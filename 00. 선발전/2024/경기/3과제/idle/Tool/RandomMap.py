from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        for i in range(2):
            m = ['x' if i in [0,2,4,10,12,14,20,22,24] else '0' for i in range(25)]
            for pk in '123456789abc':
                p = c([i for i in range(25) if m[i] == '0'])
                m[p] = pk
            res.append(''.join(m))
    if t == 1:
        m = ['x' if i in [0,3,12,15] else '0' for i in range(16)]
        for pk in '12345678':
            p = c([i for i in range(16) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
        m = ['x' if i in [0,3,12,15] else '0' for i in range(16)]
        for pk in '12345678':
            p = c([i for i in [1,2,4,7,8,11,13,14] if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 2:
        m = ['0']*8
        for pk in '123456':
            m[c([i for i in range(8) if (i < 2 or m[i - 2] != '0') and m[i] == '0'])] = pk
        res.append(''.join(m))
    return res

# m1,m2 = randomMap(0)
# prt(m1,5,5)
# prt(m2,5,5)

# m1,m2 = randomMap(1)
# prt(m1,4,4)
# prt(m2,4,4)

# m, = randomMap(2)
# prt(m,1,2,4)