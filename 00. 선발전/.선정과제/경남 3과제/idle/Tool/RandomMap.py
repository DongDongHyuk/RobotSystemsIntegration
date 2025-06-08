from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        x = cs(range(12),c([0,1]))
        h = cs([i for i in range(12) if i not in x],c([0,1]))
        h=[]
        for i in range(2):
            m = ['x' if i in x else '0' for i in range(12)]
            for pk in '1234567':
                m[c([i for i in range(12) if m[i] == '0' and i not in h])] = pk
            res.append(''.join(m))
        res.append(h)
    if t == 1:
        x = cs(range(8),c([0,1]))
        st = '12345678'[:c([7,8-len(x)])]
        for i in range(2):
            m = ['x' if i in x else '0' for i in range(8)]
            for pk in st:
                m[c([i for i in range(8) if m[i] == '0'])] = pk
            res.append(''.join(m))
    if t == 2:
        pass
    return res

# m1,m2,hli = randomMap(0)
# print(hli)
# prt(m1,3,4)
# prt(m2,3,4)

# m1,m2 = randomMap(1)
# prt(m1,1,8)
# prt(m2,1,8)