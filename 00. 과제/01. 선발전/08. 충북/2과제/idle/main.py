from time import time
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Tool.Printer import prt

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    if t == 0 and abs(s-e) not in [1,5]:
        r = [e,12,s]
    else:
        r = [e,s] if li == -1 else li
    info = [r,10 if m[s] == 'a' else int(m[s])]
    return [''.join(m),info]

def aro(p):
    li = [7,11,13,17] if t == 0 else []
    li1 = [i for i in li if i != p] if p in li else []
    dxy = [-sx,1,sx,-1]
    li = ([(0,1,2,3,4),(4,9,14,19,24),(20,21,22,23,24),(0,5,10,15,20)] if t == 0 else 
          [(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)])
    return li1+[p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1,tf=''):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or fx[i]:
            continue
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0]+tf and not fx[j]]:
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a,res1=-1,tf=''):
    global res,mkdCt        # temp
    if n == -2:
        s, = a
        li = []
    if n in [-1,-3,-4]:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        p,pk = a
    q = [m if n > 0 else s]
    mkd,step = {q[0]:-1},{q[0]:-1}
    while 1:
        if n == -2 and not q:
            return li
        if n == -1 and (len(q) > 1 or not q):
            break
        cur = q.pop(0)
        if n > 0:       # temp
            mkdCt += 1
        if n == -4 and m[cur] == '0':
            break
        if n == -3 and m[cur] != '0':
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pk == -1 and cur == p) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur,tf):
            if i not in mkd:
                if n == -2:
                    li.append(i)
                q.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n > 0:
        res1 = res1 if res1 != -1 else res
        res1 += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]

def sort(m,e,pk):
    global res
    if m[e] == pk:
        fx[e]=1
        return m
    def emt(m,p,res1=-1):
        r = src(-4,m,p,tf=pk)
        for i in r[::-1]+[p]:
            m = src(1,m,i,'0',tf=pk,res1=res1)
        return m
    def chk(m,p):
        res1 = []
        m1 = m[:]
        m1 = emt(m1,p,res1=res1)
        m1 = src(1,m1,p,pk,res1=res1)
        ct = len([i for i in [e]+src(-2,m1,e,tf=pk) if m1[i] == '0'])
        return ct,m1,res1
    def move(m,li):
        global res
        li1 = []
        for i in li:
            fx[i]=1
            li1.append((i,src(-2,m,e)))
            fx[i]=0
        li = max(li1,key=lambda i:len(i[1]))
        for i in src(0,m,s,li[0]):
            ct,m1,res1 = chk(m,i)
            res += res1
            m = m1[:]
        return m
    r = src(-1,m,e)
    ctz = m.count('0')-(3 if t == 0 else 0)
    while m[e] != pk:
        s = m.index(pk)
        cs = src(0,m,s,e)[0]
        ct = len([i for i in [e]+src(-2,m,e,tf=pk) if m[i] == '0'])
        if ct < 2 and not (cs == e and m[e] == '0'):
            m = move(m,[i for i,j in exp(0,m,s) if i != e])
            continue
        ct,m1,res1 = chk(m,cs)
        if ct < 2 and not (cs == e and m[e] == '0') and not (cs == e and ct > -1):
            m = move(m,[s]+[i for i,j in exp(0,m,cs) if i != s])
            s = m.index(pk)
            r1 = src(0,m,s,e)[:ctz]
            for i in r1[::-1]:
                m = emt(m,i)
                fx[i]=1
            fxli(r1,0)
            for i in r1:
                m = src(1,m,i,pk)
            continue
        res += res1
        m = m1[:]
    fx[e]=1
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,res
    t = g_t
    sy,sx = [5,5] if t == 0 else [4,4]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    res = []
    if t == 0:
        leaf = '1x0x23000450006700089x0xa'
        fxli([2,12,22],1)
        li = [0,5,20,15,10,4,9,24,19,14]
        for i in li:
            m = sort(m,i,leaf[i])
    if t == 1:
        leaf = '1234567800000000'
        li = [0,1,2,3]+([7,6,5,4] if m[10]=='x' else [4,5,6,7])
        for i in li:
            m = sort(m,i,leaf[i])
    if t == 2:
        m1 = m[:]
        m2,leaf1 = a
        leaf2 = ''.join([leaf1[i] for i in [3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12]])
        for m,leaf in [[m1,leaf1],[m2,leaf2]]:
            li = [12,13,14,15,8] if m.index('x') in [5,6] else [0,1,2,3,4]
            li1 = []
            for i in li:
                pk = leaf[i]
                if leaf[i] == '0':
                    r = src(-3,''.join(leaf),i)
                    p = r[-1]
                    pk = leaf[p]
                m = sort(m,i,pk)
                if leaf[i] == '0':
                    leaf,info = exc(leaf,i,p,[i]+r)
                    li1.append(info)
            fx={i:0 for i in fx}
            res += li1[::-1]
            res.append([[-1,-1],-1])
    return res

mkdCt = 0       # temp
if __name__ == '__main__':
    t,m1 = 1,'0000050807x16342'
    t,m1,m2,m3 = 2,'10300x0402000005','000042x513000000','00000x0000051234'

    t,m1 = 0,'2x0xa7000890004600015x0x3'
    
    ts = time()
    res = main(t,m1) if t < 2 else main(t,m1,m2,m3)
    te = time() - ts
    # for i in res:
    #     if type(i) == str: 
    #         prt(i,4,4)
    #     else:
    #         print(i)
    print(res)
    print('visited :',mkdCt)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))