from time import time
from Tool.Printer import *
from queue import *

def exc(m,s,e,r):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [r,int(m[s])]
    return [''.join(m),info]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx,dz = [-1,0,1,0,0,0],[0,1,0,-1,0,0],[0,0,0,0,-1,1]
    y,x,z = (pos // sx) % sy, pos % sx, pos // size 
    for i in range(6):
        ny,nx,nz = y + dy[i],x + dx[i],z + dz[i]
        if -1 < ny < sy and -1 < nx < sx and -1 < nz < sz:
            res.append((size * nz) + ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,p=-1):
    res = []
    for i in range(size * sz) if n > 0 else [p]:
        if fx[i] or m[i] == 'x' or (n > 0 and m[i] == '0'):
            continue
        if n == -3 and m[i] != '0':
            continue
        if t == 1 and n > 0 and (i < 9 and m[i + 9] != '0'):
            continue
        di = src(-1,m,i,-1) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            if t == 1 and n > 0 and (i%size == j%size or (j > 8 and m[j - 9] == '0')):
                continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

vs = 0
def src(n,m,*a):
    global res
    global vs       # temp
    if n < 1:
        s,e = a
        if n in [0,-2] and (n,s,e) in cache:
            return cache[n,s,e]
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}    
    def heu0(m):
        ct = 0
        if p != -1:
            e = p
            di = {}
            for i in range(size*sz):
                if m[i] == pk and not fx[i]:
                    di[i] = len([i for i in src(0,m,i,e) if m[i] not in '0'+pk])            
            s = min(di,key=lambda n:di[n])
            rp = di[s]            
            ct += 10000 * rp
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size*sz):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p != -1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst ** 2
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    def heu1(m):
        ct1,ct2 = 0,0
        for i in range(9):
            di = {'00':0,'10':1,'11':1,'21':1,'20':2,'22':2,'12':3}
            pk = str(di[m[i]+m[i+9]])
            ct1 += pk == v1[i]
            ct2 += v1[i] == '2' and m[i] == '2'
            ct2 += v1[i] == '3' and m[i] == '1'
        for i in range(6):
            for j in range(3):
                n = [6,7,8,15,16,17][i]-(3*j)
                if m[n] != '0':
                    break
            ct1 += m[n] == v2[i]
        for i in range(6):
            for j in range(3):
                n = [8,5,2,17,14,11][i]-j
                if m[n] != '0':
                    break
            ct1 += m[n] == v3[i]
        return [ct1 == 21,((-100 * ct1) + (-100 * ct2))]
    def put(cur):
        if n > 0:
            h = heu1(cur)[1] if t == 1 else heu0(cur)
            q.put((g[cur] + h, cur))
        else:
            q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.pop(0)
    put(cur)
    while 1:
        if n == -2 and len(q) > 1:      # default
            break
        if n in [0,-1] and not q:      # default
            return mkd
        cur = get()
        if n > 0:      # temp
            vs += 1
        if n == -3 and m[cur] != '0' and cur not in e:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break        
        if n == 2 and heu1(cur)[0]:
            break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                mkd[i] = mkd[cur] + [j]
                g[i] = g[cur] + 1
                put(i)
    res1 = mkd[cur]
    if n > 0:
        res += res1[1:]
        return cur
    if n in [0,-2]:
        cache[n,s,e] = res1
    return res1

def main(g_t,m,*a):
    global t,sy,sx,sz,size,fx,fxli,cache,res
    t = g_t
    sy,sx,sz = [3,3,1] if t == 0 else [3,3,2] if t == 1 else [4,4,1]
    size = sy * sx
    fx = {i:0 for i in range(size * sz)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        leaf = '123456700'
        src(1,m,leaf,-1,-1)
    if t == 1:
        global v1,v2,v3
        v1,v2,v3 = a
        print(v1,v2,v3)
        for i in range(9):
            pk = v1[i]
            if pk in '23':
                m = src(1,m,-1,i,{'2':'2','3':'1'}[pk])
                fx[i] = 1
        m = src(2,m)
    if t == 2:
        leaf,=a
        li = [i for i in [0,3,12,15] if m[i] != 'x']
        hd,hdr = [],{}
        leaf1 = list(leaf[:])
        for i in li:
            pk = leaf1[i]
            if pk == '0':
                r = src(-3,leaf1,i,hd)
                pk = leaf1[r[-1]]
                hd.append(i)
                hdr[i] = r
                leaf1[r[-1]],leaf1[i] = '0',pk
            m = src(1,m,''.join(leaf1),i,pk)
            fx[i] = 1
        m = src(1,m,''.join(leaf1),-1,-1)
        for i in hd[::-1]:
            res.append([hdr[i],int(m[i])])
    return res

if __name__ == '__main__':

    t,m = 0,'207450316'
    t,m,v1,v2,v3 = 1,'111002221120002201','120133302','112222','212222'
    t,m,v1,v2,v3 = 1,'021121102''002122100','103''302''021','121''221','121''122'
    t,m,v1,v2,v3 = 1,'102110211200200221','111023132','112022','211220'
    # t,m1,m2 = 2,'103005x008026470','850001x427600030'

    ts = time()
    res = main(t,m) if t == 0 else main(t,m,v1,v2,v3) if t == 1 else main(t,m1,m2)
    te = time() - ts
    print(res)
    print('visited :',vs)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
