from time import time
from Tool.Printer import *

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    r = [e,s] if li == -1 else li
    con = lambda n: 10 if n == 'a' else int(n)
    info = [r,con(m[s])]
    if t == 0 and m[e] != '0':
        info = [[e,s],[con(m[e]),con(m[s])]]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2,9,10,11),(2,5,8,11,14,17),(6,7,8,15,16,17),(0,3,6,9,12,15)],[],[]][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    if t == 0 and n > 0:      # A
        for i,j in [[i,j] for i in range(9) for j in range(9,18)]:
            if fx[i] or fx[j] or m[j] in '0x':
                continue
            if i in hli or (i+9 != j and m[i+9] != '0'):
                continue
            if [st for st in ['12345','6789a'] if m[i] not in st and m[j] not in st]:
                continue
            res.append(exc(m,i,j))
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or fx[i]:        # default
            continue
        if t == 0 and n > 0:      # A
            if i in hli or (i > 8 and m[i-9] == '0'):
                continue
        for j in aro(i):
            if t == 0 and j % 8 in hli:         # A
                j, = [k for k,_ in exp(0,m,j) if k != i]
                res.append(exc(m,i,j,hli[0]))
                continue
            if m[j] in ['x','0x'][n > 0] or fx[j]:      # default
                continue
            if t == 0 and n > 0 and (i < 9 or j < 9):       # A
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a):
    global res
    if n == 0:
        s,e = a
    if n == 1:
        p,pk = a
    if n == 2:
        p,st = a
    q = [m if n > 0 else s] 
    mkd = {i:[] for i in q}
    while 1:
        cur = q.pop(0)
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pk == -1 and cur == p) or (pk != -1 and cur[p] == pk):
                break
        if n == 2 and cur[p] in st:
            break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                q.append(i)
                mkd[i] = mkd[cur] + [j]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    r = src(0,m,m.index(pk),p)
    for i in r:
        m = src(1,m,i,pk)
    fx[p] = 1
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,res
    t = g_t
    sy,sx = [[3,3],[None,None],[None,None]][t]
    size = sy * sx * (2 if t == 0 else 1)
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    res = []
    if t == 0:
        global hli
        leaf,hli = a

        # print(hli)
        # prt(m1,3,3,2)
        # prt(m2,3,3,2)
        # exit()

        # li = ['12345','6789a']
        # n = 0
        # while len([i for i in fx if fx[i]]) < 2:
        #     p = [i for i in range(9) if m[i] != leaf[i] and leaf[i] in li[n]][0]
        #     pk = leaf[p]
        #     if pk in li[n]:
        #         n = 1 - n
        #         if m[p] != pk:
        #             m = src(2,m,p,li[n])
        #             m = src(1,m,p,leaf[p])
        #         fx[p] = 1
        m = src(1,m,leaf,-1)


    return res

if __name__ == '__main__':
    t,m1,m2,hli = 0,'7654x3210a980x0000','1234x567089a0x0000',[8]
    t,m1,m2,hli = 0,'4730x62519080xa000','4760x12350a80x9000',[3]
    t,m1,m2,hli = 0,'1234x567089a0x0000','1234x5670a980x0000',[8]

    ts = time()
    res = main(t,m1,m2,hli) if t == 0 else None
    te = time() - ts
    # for i in res:
    #     prt(i,3,3,2)
    print(res)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
