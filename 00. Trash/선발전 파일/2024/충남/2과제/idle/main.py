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
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if fx[i] or m[i] == 'x' or (n > 0 and m[i] == '0'):
            continue
        di = src(-1,m,i,-1) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

def src(n,m,*a):
    global res
    if n < 1:
        s,e = a
        if n in [0,-2] and (n,s,e) in cache:
            return cache[(n,s,e)]
    if n == 1:
        leaf,p,pk = a
    if n == 2:
        p,li = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}
    def heu(m):
        ct = 0
        if n == 2:
            for i in range(size):
                if m[i] not in  '0x':
                    y1,x1 = divmod(i,sx)
                    y2,x2 = divmod(p,sx)
                    ct -= (abs(y1-y2) + abs(x1-x2))
            ct -= 10 * len([i for i in li if m[i] != '0'])
            return ct
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
        used = []
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                if p == -1:
                    p1 = [j for j in range(25) if j not in used and leaf[j] == m[i]][0]
                    used.append(p1)
                    y2,x2 = divmod(p1,sx)
                else:
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
        if n == -3 and m[cur] != '0' and cur not in e:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        if n == 2 and all([cur[i] != '0' for i in li]):
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
        cache[(n,s,e)] = res1
    return res1

def main(g_t,m,*a,mod=0):
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [4,4] if t < 2 else [5,5]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t < 2:
        ptr,=a
        ptr = ptr[0]
        m = src(1,m,-1,ptr,'1')
        res.append(-1)
        m = list(m)
        m[m.index('1')] = '0'
        for i in range(4):
            di = {i:src(-1,m,i,-1) for i in range(16) if m[i] not in '01x'}
            li = min([di[i][ptr] for i in di if ptr in di[i]],key=len)
            res.append([li,int(m[li[0]])])
            m[li[0]] = '0'
    if t == 2:
        if mod == 0:
            ptr,=a
            for i in range(2):
                di = src(-1,m,ptr[i],-1)
                li = [di[i] for i in sorted(di,key=lambda n:len(di[n]))][:4]
                fxli([i[-1] for i in li],1)
                res.append(li[:4][::-1])
        if mod == 1:
            li = [i for i in range(25) if m[i] == '2']
            fxli(li,1)
            for i in range(2):
                p = li[i]
                m = src(2,m,p,aro(p))
                m = list(m)
                m[i] = '0'
                m = ''.join(m)
                fx[i] = 0
                res.append(-1)
        if mod == 2:
            leaf,=a
            li = []
            while len(li) < 11:
                li1 = [i for i in range(25) if m[i] != 'x' and not fx[i] and i not in li]
                li.append(min(li1,key = lambda n:len(exp(0,m,n))))
                fxli(li,1)
            fxli(li,0)
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

    t,m,ptr = 0,'x04000x050050041',[9]
    t,m,ptr,mod = 2,'x000x00200000000020000000',[10,20],0
    t,m,mod = 2,'x000x''40200''44000''54200''55500',1
    # t,m1,m2,mod = 2,None,'x050x04540034005550304500',2

    ts = time()
    if t < 2:
        res = main(t,m,ptr)
    else:
        res = main(t,m1,m2,mod=2) if mod == 2 else main(t,m,mod=1) if mod == 1 else main(t,m,ptr,mod=0)
    te = time() - ts
    print(res)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
