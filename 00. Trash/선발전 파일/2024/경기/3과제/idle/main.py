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
        info = [r,di[m[s]] if m[s] in di else int(m[s])]
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

def exp(n,m,p=-1,leaf=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if fx[i] or m[i] == 'x':
            continue
        if t == 2:
            if m[i] != '0' and m.count('0') < 4 and (i > 5 or m[i+2]=='0'):
                res.append(exc(m,-1,-1,-1,i,-1))
            if m[i] == '0' and (i < 2 or m[i-2] != '0'):
                for pk in leaf:
                    if pk not in m:
                        res.append(exc(m,-1,-1,-1,i,pk))
            continue
        if (n > 0 and m[i] == '0'):
            continue
        di = src(-1,m,i,-1) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

mkdCt = 0
def src(n,m,*a):
    global res,mkdCt
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
        if t == 2:
            return 0   
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
                y2,x2 = divmod(p,sx)
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
        if n > 0:
            mkdCt += 1
        if n == -3 and m[cur] not in '0' + e:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur,leaf if n == 1 else -1):
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
    sy,sx = [[5,5],[4,4],[4,2]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t < 2:
        leaf,=a
        li = [[1,3,5,9,15,19,7,6,8,11,13],[1,2,4,8,7,11,13,14]][t]
        hd,hdr = [],{}
        leaf1 = list(leaf[:])
        for i in li:
            pk = leaf1[i]
            if pk == '0':
                r = src(-3,leaf1,i,''.join(hd))
                pk = leaf1[r[-1]]
                hd.append(pk)
                hdr[pk] = r
                leaf1[r[-1]],leaf1[i] = '0',pk
            m = src(1,m,''.join(leaf1),i,pk)
            fx[i] = 1
        m = src(1,m,''.join(leaf1),-1,-1)
        for i in hd[::-1]:
            di = {'a':10,'b':11,'c':12}
            res.append([hdr[i],di[pk] if pk in di else int(pk)])
    else:
        li = sorted(map(int,m))[2:]
        leaf = ''.join([str(li[i]) for i in [4,5,2,3,0,1]])+'00'

        for i in range(6):
            m = src(1,m,leaf,i,leaf[i])
            fx[i] = 1

    return res

if __name__ == '__main__':

    t,m1,m2 = 0,'x3x5x190a2xcx0x60b07x8x4x','x5x6x21b97x8xcx30a04x0x0x'
    # t,m1,m2 = 1,'x10x05483726x00x','x21x30086004x75x'
    # t,m = 2,'12''34''56''00'

    ts = time()
    res = main(t,m1,m2) if t < 2 else main(t,m)
    te = time() - ts
    print(res)
    print('visit :',mkdCt)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
