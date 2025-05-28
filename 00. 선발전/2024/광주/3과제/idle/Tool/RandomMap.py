from random import choice as c, sample as cs
from Printer import prt

def view(m):
    view1,view2,view3 = [],[],[]
    for i in range(9):
        li1 = ['10','11','21']
        li2 = ['20','22']
        st = m[i]+m[i+9]
        pk = '0' if st == '00' else '1' if st in li1 else '2' if st in li2 else '3'
        view1.append(pk)
    for i in range(6):
        for j in range(3):
            n = [6,7,8,15,16,17][i]-(3*j)
            if m[n] != '0':
                break
        view2.append(m[n])
    for i in range(6):
        for j in range(3):
            n = [8,5,2,17,14,11][i]-j
            if m[n] != '0':
                break
        view3.append(m[n])
    return list(map(''.join,[view1,view2,view3]))

def randomMap(t):
    res = []
    if t == 0:
        m = ['0']*9
        for pk in '123456700':
            p = c([i for i in range(9) if m[i] == '0'])
            m[p] = pk
        res.append(''.join(m))
    if t == 1:
        for i in range(2):
            m = ['0']*18
            for pk in '111111222222':
                p = c([i for i in range(18) if m[i] == '0' and (i < 9 or m[i -9] != '0')])
                m[p] = pk
            if i:
                res += view(''.join(m))
            else:
                res.append(''.join(m))
            
    if t == 2:
        x = c(range(16))
        for i in range(2):
            m = ['0'] * 16
            m[x] = 'x'
            for pk in '12345678':
                p = c([i for i in range(16) if m[i] == '0'])
                m[p] = pk
            res.append(''.join(m))
    return res

# m = randomMap(0)
# prt(m,3,3)

# m1,view1,view2,view3 = randomMap(1)
# print(view1,view2,view3)
# prt(m1,3,3,2)

# m1,m2 = randomMap(2)
# prt(m1,4,4)
# prt(m2,4,4)