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
        if n != -1 and (n,s,e) in cache:
            return cache[(n,s,e)]
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}    
    def heu(m):
        ct = 0
        if p != -1:
            e = p
            di = {}
            for i in range(size):
                if m[i] == pk and not fx[i]:
                    di[i] = len([i for i in src(0,m,i,e) if m[i] not in '0'+pk])            
            s = min(di,key=lambda n:di[n])
            rp = di[s]            
            ct += 10000 * rp
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p != -1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    put = lambda cur: q.put((g[cur] + heu(cur), cur)) if n > 0 else q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.pop(0)
    put(cur)
    while 1:
        if n == -2 and len(q) > 1:      # default
            break
        if n in [0,-1] and not q:      # default
            return mkd
        cur = get()
        if n == 1:      # temp
            vs += 1
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
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
    if n != -1:
        cache[(n,s,e)] = res1
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
        src(1,m,'123456700',-1,-1)
    if t == 1:
        ft,rt = a
        leaf = ''

        # for i,j in exp(1,m):
        #     print(j)
        #     prt(i,3,3,2)

        prt(''.join(leaf),3,3,2)

    return res

if __name__ == '__main__':

    t,m = 0,'471620503'
    t,m,ft,rt = 1,'111002221120002201','112222','212222'

    ts = time()
    res = main(t,m) if t == 0 else main(t,m,ft,rt) if t == 1 else main
    te = time() - ts
    print(res)
    print('visited :',vs)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
