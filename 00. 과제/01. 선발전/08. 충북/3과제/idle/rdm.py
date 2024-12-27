import random
from printer import prt

def rdm(t):
    res = []
    c = random.choice
    cs = random.sample
    if t == 0:
        hli = cs(range(25),3)
        xli = None
        while xli == None or sorted(xli) in [[1,5],[3,9],[15,21],[19,23]]:
            xli = cs([i for i in range(25) if i not in hli],2)
        for i in range(2):
            m = ['0']*25
            for pk in '12345678':
                p = c([i for i in range(25) if i not in xli + hli and m[i] == '0'])
                m[p] = pk
            m = ['x' if i in xli else m[i] for i in range(25)]
            res.append(''.join(m))
        res.append(hli)
    if t == 1:
        pass
    if t == 2:
        pass
    return res