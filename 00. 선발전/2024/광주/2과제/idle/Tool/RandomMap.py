from random import choice as c, sample as cs
from Printer import prt

def aro(p):
    dxy = [-4,1,4,-1]
    li = [(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(p):
    res = []
    for i in [p]:
        if i in hli:
            continue
        for j in aro(i):
            if j in hli:
                isg = j == hli[0]
                li = [k for k in aro(j) if k not in xhli+[i] and (abs(i-j) == abs(j-k) == (1 if isg else 4))]
                if not li:
                    continue
                j = li[0]
            if j in xhli:
                continue
            res.append(j)
    return res

def randomMap(t):
    res = []
    if t == 0:
        global hli,xhli
        x = c([i for i in range(16)])

        while 1:
            h1 = c([i for  i in range(16) if i not in aro(x)+[x]])
            h2 = c([i for  i in range(16) if i not in aro(x)+aro(h1)+[x,h1]])
            hli = [h1,h2]
            xhli = hli+[x]
            li = [x,h1,h2]
            for i in range(16):
                if i in xhli:
                    continue 
                if len(exp(i)) == 0:
                    break
                if li in [[5,8,2],[6,11,1],[9,4,14],[10,7,13]]:
                    break
            else:
                break

        for i in range(2):
            m = ['0']*16
            m[x] = 'x'
            for pk in '12345678':
                p = c([i for i in range(16) if m[i] == '0' and i not in hli])
                m[p] = pk
            res.append(''.join(m))
        res.append(hli)
    if t == 1:
        m1 = ['0']*15
        m2 = ['0']*15
        m3 = ['0']*15
        x = c(range(15))
        m1[x] = 'x'
        m3[x] = 'x'
        m2[c(range(15))] = 'x'
        hli = [[c([i for i in range(15) if m1[i] == '0'])],[c([i for i in range(15) if m2[i] == '0'])]]
        for pk in '123456789abcdefghi':
            m = [m1,m2]
            n = c([i for i in range(2) if [j for j in range(15) if m[i][j] == '0' and j not in hli[i]]])
            m = m[n]
            p = c([i for i in range(15) if m[i] == '0' and i not in hli[n]])
            m[p] = pk   
        for i in range(c(range(14))):
            p = c([i for i in range(15) if m3[i] == '0' and i not in hli[0]])
            pk = c([i for i in '123456789abcdefghi' if i not in m3])
            m3[p] = pk
        res.append(''.join(m1))
        res.append(''.join(m2))
        res.append(''.join(m3))
        res.append(hli)
    if t == 2:
        for i in range(2):
            m = ['0']*9
            for pk in '1234567':
                p = c([i for i in range(9) if m[i] == '0'])
                m[p] = pk
            res.append(''.join(m))
    return res

# m1,m2,hli = randomMap(0)
# print(hli)
# prt(m1,4,4)
# prt(m2,4,4)

# m1,m2,m3,hli = randomMap(1)
# print(hli)
# prt(m1,5,3)
# prt(m2,5,3)
# prt(m3,5,3)

# m1,m2 = randomMap(2)
# prt(m1,3,3)
# prt(m2,3,3)