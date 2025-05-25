from random import choice as c, sample as cs
from Printer import prt

def randomMap(t):
    res = []
    if t == 0:
        while 1:
            m = ['0']*16
            for pk in '123':
                di = {1:4,4:1,2:7,7:2,8:13,13:8,11:14,14:11}
                li = [i for i in range(16) if all([m[y*4+(i%4)] == '0' for y in range(4)]) and all([m[(i//4)*4+x] == '0' for x in range(4)])]
                li = [i for i in li if i not in di or m[di[i]] == '0']
                m[c(li)] = pk
            info = [m.index('1'),m.index('2'),m.index('3')]
            no = [[1,6,11],[2,5,8],[4,9,14],[7,10,13]]
            if sorted([i for i in range(16) if m[i] != '0']) not in no:
                break
        for pk in '112233':
            p = c([i for i in range(16) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
        res.append(info)
    if t == 1:
        li = [0,4,15,19]
        li.append(c([5,10]))
        li.append(c([9,14]))
        li += cs([1,2,3,16,17,18],3)
        m = ['x' if i in li else '0' for i in range(20)]
        for pk in '123456':
            m[c([i for i in [6,7,8,11,12,13] if m[i] == '0'])] = pk
        res.append(''.join(m))
    if t == 2:
        hli = cs([i for i in range(25)],2)
        for i in range(2):
            m = ['0']*25
            for pk in '1234':
                p = c([i for i in range(25) if m[i] == '0' and i not in hli])
                m[p] = pk
            for pk in '56':
                p = c([i for i in range(25) if m[i] == '0' and i not in hli and  not i%2])
                m[p] = pk
            for pk in '78':
                p = c([i for i in range(25) if m[i] == '0' and i not in hli and  i%2])
                m[p] = pk
            res.append(''.join(m))
        res.append(hli)
    return res

# m,fix = randomMap(0)
# print(fix)
# prt(m,4,4)

# m, = randomMap(1)
# prt(m,4,5)

# m1,m2,hli = randomMap(2)
# print(hli)
# prt(m1,5,5)
# prt(m2,5,5)