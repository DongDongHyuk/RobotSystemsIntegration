from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        hli = [c([0,1,2,3,4,6,7,8])]
        for i in range(2):
            m = ['0']*18
            m[4],m[13] = 'x','x'
            for i in range(10):
                p = c([j for j in (range(9) if i < 7 else range(9,18)) if j not in hli and m[j] == '0' and (j < 9 or m[j - 9] != '0')])
                pk = [i for i in '123456789a' if i not in m][0]
                m[p] = pk
            res.append(''.join(m))
        res.append(hli)
    if t == 1:
        for i in range(2):
            m = ['0']*16
            m[0],m[3],m[12],m[15] = 'x'*4
            li = [[1,2,5,6],[6,7,10,11],[9,10,13,14],[4,5,8,9],[5,6,9,10]]
            li1 = []
            for i in range(3):
                p = c([i for i in range(16) if m[i] == '0' and i not in li1])
                m[p] = 'x'
                for j in li:
                    if [k for k in j if m[k] == 'x']:
                        li1 += j
            for pk in '123456':
                p = c([i for i in range(16) if m[i] == '0'])
                m[p] = pk
            res.append(''.join(m))
    if t == 2:
        for i in range(2):
            m = ['0']*15
            m[7] = 'x'
            hli = c([[6,8],[8,6]])
            for pk in '123456789':
                p = c([i for i in range(15) if m[i] == '0' and i not in hli])
                m[p] = pk
            res.append(''.join(m))
    return res

# m1,m2,hli = randomMap(0)
# prt(m1,3,3,2)
# prt(m2,3,3,2)

# m1,m2 = randomMap(1)
# prt(m1,4,4)
# prt(m2,4,4)

# m1,m2 = randomMap(2)
# prt(m1,5,3)
# prt(m2,5,3)