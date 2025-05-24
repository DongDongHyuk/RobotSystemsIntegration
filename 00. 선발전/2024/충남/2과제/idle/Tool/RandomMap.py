from random import choice as c, sample as cs
from Printer import prt
def aro(pos):
    res = []
    sy,sx = 5,5
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    return res

def randomMap(t,mod=0):
    res = []
    if t < 2:
        ptr = [c(range(16))]
        while 1:
            x = cs([i for i in range(16) if i not in ptr],2)
            if sorted(x) not in [[1,4],[2,7],[8,13],[11,14]]:
                break
        m = ['x' if i in x else '0' for i in range(16)]
        for pk in '14455':
            m[c([i for i in range(16) if i not in ptr+x and m[i] == '0'] )] = pk
        res.append(''.join(m))
        res.append(ptr)
    else:
        if mod < 2:
            m = ['0']*25
            for i in range(2):
                while 1:
                    li = []
                    for j in range(25):
                        if (m[j] != '0' or  len([j for j in aro(j) if m[j] == '0']) != 4):
                            continue
                        li.append(j)
                    if li:
                        m[c(li)] = '2'
                        break
            while 1:
                x = cs([i for i in range(25) if m[i] == '0' and not any([m[j] == '5' for j in aro(i)])],2)
                if sorted(x) not in [[1,5],[3,9],[15,21],[19,23]]:
                    break
            for i in x:
                m[i] = 'x'
            if mod == 1:
                for pk in '44445555':
                    m[c([i for i in range(25) if m[i] == '0'])] = pk
            res.append(''.join(m))
            if mod == 0:
                res.append(cs([i for i in range(25) if m[i] == '0' and not any([m[j] == '5' for j in aro(i)])],2))
            res.append(mod)
        else:
            while 1:
                x = cs(range(25),2)
                if sorted(x) not in [[1,5],[3,9],[15,21],[19,23]]:
                    break
            for i in range(2):
                m = ['x' if i in x else '0' for i in range(25)]
                for pk in '334444555555':
                    m[c([i for i in range(25) if m[i] == '0'])] = pk
                res.append(''.join(m))
            res.append(1)
    return res

# m,ptr = randomMap(0)
# print(ptr)
# prt(m,4,4)

# m,ptr,mod = randomMap(2,mod = 0)
# print(mod)
# print(ptr)
# prt(m,5,5)

# m,mod = randomMap(2,mod = 1)
# print(mod)
# prt(m,5,5)

# m1,m2,mod = randomMap(2,mod = 2)
# print(mod)
# prt(m1,5,5)
# prt(m2,5,5)