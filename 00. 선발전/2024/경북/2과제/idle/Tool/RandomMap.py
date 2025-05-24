from random import choice as c, sample as cs, shuffle as sf
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        m = ['0']*12
        for pk in '123456798abc':
            p = c([i for i in range(12) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 1:
        m = ['0']*9
        for pk in '123456':
            p = c([i for i in range(9) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 2:
        m = ['0']*15
        hli = [2,7,12]
        sf(hli)
        for pk in '123456':
            p = c([i for i in [1,3,6,8,11,13] if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
        res.append(hli)
    if t == 3:
        m1 = ['0']*9
        m2 = ['0']*9
        for pk in '123456':
            n = c([0,1])
            [m1,m2][n][c([i for i in range(9) if [m1,m2][n][i] == '0'])] = pk
        for pk in '789abc':
            n = c([i for i in range(2) if [m1,m2][i].count('0') > 3])
            [m1,m2][n][c([i for i in range(9) if [m1,m2][n][i] == '0'])] = pk
        res.append(''.join(m1))
        res.append(''.join(m2))
    return res

# m, = randomMap(0)
# prt(m,1,6,2)

# m, = randomMap(1)
# prt(m,3,3)

# m,hli = randomMap(2)
# print(hli)
# prt(m,3,5)

m1,m2 = randomMap(3)
prt(m1,3,3)
prt(m2,3,3)