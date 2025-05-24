from time import time
from Tool.Printer import *
from queue import *

def exc(m,s,e,r,p=-1,pk=-1):
    m = list(m)
    di = {'abc'[i-10] if i > 9 else str(i):i for i in range(1,13)}
    if p != -1:
        n = int(pk == -1)
        info = [n,p,di[m[p] if n else pk]]        # n,p,pk
        m[p] = '0' if n else pk
    else:
        m[s],m[e] = m[e],m[s]
        info = ([ing] if t == 3 else [])+[r,di[m[s]]]
    return [''.join(m),info]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,p=-1,pk=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if fx[i] or m[i] == 'x':         # default
            continue
        if t == 0:
            if m[i] != '0' and m.count('0') < 2 and (i > 5 or m[i + 6]=='0'):
                res.append(exc(m,-1,-1,-1,i,-1))
            if m[i] == '0' and '0' in m and (i < 6 or m[i-6] != '0'):
                for pk in '123456789abc':
                    if pk not in m:
                        res.append(exc(m,-1,-1,-1,i,pk))
            continue
        if (n > 0 and m[i] == '0'):         # default
            continue
        di = src(-1,m,i,m[i]) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            if t == 2:
                if n > 0 and j in hli:
                    continue
                if n == -1 and ((j == hli[0] and pk not in '14') or (j == hli[1] and pk not in '25') or (j == hli[2] and pk not in '36')):
                    continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

mkdCt=0
def src(n,m,*a):
    global res,mkdCt
    if n == -1:
        s,pk = a
    if n in [0,-2]:
        s,e = a
        if (n,s,e) in cache:
            return cache[(n,s,e)]
    if n == 1:
        leaf,p,pk = a
    if n == 2:
        li,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}
    def heu0(m,isDead=0,r2=[]):
        ct = 0
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p != -1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst
        return ct
    def heu1(m):
        ct = 0
        s = m.index(pk)
        rp = len([i for i in src(0,m,s,p) if m[i] not in '0'+pk])
        ct += 10000 * rp
        r2 = src(-2,m,p,-1)
        isDead = len(r2) > 1
        ct += heu0(m,isDead,r2)            
        if not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    def heu2(m):
        ct = 0
        for pk in '123456789abc':
            p = leaf.index(pk)
            if m[p] != pk and pk not in m:
                if p < 6 and m[p + 6] == '0':
                    ct -= 100
                if m[p] == '0':
                    ct -= 100
            if (p < 6 and m[p] == pk) or (p > 5 and m[p - 5] == leaf[p - 5] and m[p] == pk):
                ct -= 1000
        return ct
    def heu3(m):         # n == 2
        return -len([i for i in li if m[i] not in '0'+pk])
    def put(cur):
        if n > 0:
            heu = heu2 if t==0 else heu3 if n == 2 else (heu1 if p != -1 else heu0)
            q.put((g[cur] + heu(cur), cur))
        else:
            q.append(cur)
    def get():
        return q.get()[1] if n > 0 else q.pop(0)
    put(cur)
    while 1:
        if n == -2 and len(q) > 1:      # default
            break
        if n in [0,-1] and not q:      # default
            return mkd
        cur = get()
        if n > 0:
            mkdCt += 1
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        if n == 2 and all([cur[i] not in '0'+pk for i in li]):
            break
        for i,j in exp(n,cur if n > 0 else m,cur,pk if t == 2 and n == -1 else -1):
            if i not in mkd:
                mkd[i] = mkd[cur] + [j]
                g[i] = g[cur] + 1
                put(i)
    res1 = mkd[cur]
    if n > 0:
        res += res1[1:]
        return cur
    if n != -1:
        cache[(n,s,e)] = res1
    return res1

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [[2,6],[3,3],[3,5],[3,3]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        src(1,m,'123456cba987',-1,-1)
    if t == 1:
        src(1,m,'123456000',-1,-1)
    if t == 2:
        global hli
        hli, = a
        m = ''.join(['x' if i in [5,9] else m[i] for i in range(15)])
        leaf = '10004x205x30006'
        li1,li2 = [0,10,1,6,11],[4,14,3,8,13]
        for i in [0,10]:
            pk = leaf[i]
            li = li1 if i in li2 else li2
            for j in range(3):
                m = src(2,m,li[:j+1],pk)
            m = src(1,m,leaf,i,leaf[i])
            fx[i] = 1
        m = src(1,m,leaf,-1,-1)
        fx={i:0 for i in fx}
        src(1,m,'01040x205x03060',-1,-1)
    if t == 3:
        global m1,m2,ing
        m2, = a
        m1 = list(m[:])
        m2 = list(m2)
        di = {**{str(i):i for i in range(1,10)}, **{'a':10,'b':11,'c':12}}
        while not all([pk in m1 for pk in '123456']):
            ing = 0
            pk = [pk for pk in '789abc' if pk in m1][0]
            m1 = list(src(1,''.join(m1),-1,5,pk))
            m1[5] = '0'
            ing = 1
            m2 = list(src(1,''.join(m2),-1,7,'0'))
            m2[7] = pk
            res.append([-1,[],di[pk]])
            ing = 1
            pk = [pk for pk in '123456' if pk in m2][0]
            m2 = list(src(1,''.join(m2),-1,3,pk))
            m2[3] = '0'
            ing = 0
            m1 = list(src(1,''.join(m1),-1,1,'0'))
            m1[1] = pk
            res.append([-2,[],di[pk]])
        ing=0
        m1 = src(1,''.join(m1),'360250140',-1,-1)
        ing=1
        m2 = src(1,''.join(m2),'789abc000',-1,-1)
    return res

if __name__ == '__main__':

    t,m = 0,'2719683a4c5b'
    t,m = 1,'504310026'
    t,m,hli = 2,('050600104002030'),[2,12,7]
    # t,m1,m2 = 3,('102'
    #              'ab0'
    #              '059'),\
    #             ('460'
    #              'c37'
    #              '080')





    ts = time()
    res = main(t,m1,m2) if t == 3 else main(t,m) if t != 2 else main(t,m,hli)
    te = time() - ts
    print('visited :',mkdCt)
    print(res)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

