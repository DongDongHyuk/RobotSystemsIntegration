from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        hli = cs(range(25),3)
        while 1:
            x = cs([i for i in range(25) if i not in hli],2)
            if sorted(x) not in [[1,5],[3,9],[15,21],[19,23]]:
                break
        for i in range(2):
            m = ['x' if i in x else '0' for i in range(25)]
            for pk in '12345678':
                p = c([i for i in range(25) if m[i] == '0' and i not in hli])
                m[p] = pk
            res.append(''.join(m))
        res.append(hli)
    if t == 1:
        pass
    if t == 2:
        m = ['0']*25
        for pk in '12345678':
            p = c([i for i in range(25) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    return res


# m1,m2,hli = randomMap(0)
# print(hli)
# prt(m1,5,5)
# prt(m2,5,5)

# m = randomMap(2)
# prt(m,5,5)