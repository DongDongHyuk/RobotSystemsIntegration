from time import time
from Tool.Printer import *
from queue import PriorityQueue
from collections import deque

def exc(m,s,e,r):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [r,int(m[s])]
    return [''.join(m),info]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [[-1,0,1,0],[0,1,0,-1]] if t < 2 else [[-1,-1,-1,0,1,1,1,0],[-1,0,1,1,1,0,-1,-1]]
    y,x = divmod(pos,sx)
    for i in range(len(dy)):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def exp(n,m,p=-1,pk=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if fx[i] or m[i] == 'x' or (n > 0 and m[i] == '0'):
            continue
        if n in [-3,-4] and m[i] != '0':
            continue
        di = src(-1,m,i,-1,pk=m[i]) if n > 0 else aro(i)
        for j in di:
            if j == i or fx[j] or m[j] == 'x' or (n == -1 and m[j] != '0'):
                continue
            if t == 2:
                if n > 0 and j in hli:
                    continue
                dire = abs(j-i)
                if n < 1 and ((dire in [1,5] and pk in '5678') or (dire in [4,6] and pk in '1234')):
                    continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])
    return res

def src(n,m,*a,pk=-1):
    global res
    if n in [-4,-3]:
        s,e,li = a
    if n in [-2,-1,0]:
        s,e = a
        if n in [0,-2] and (n,s,e) in cache:
            return cache[(n,s,e)]
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else deque()
    mkd = {cur:[cur]}
    g = {cur:0}
    def heu(m):
        ct = 0
        if pk == '0':
            return 0
        if p != -1:
            e = p
            di = {}
            for i in range(size):
                if m[i] == pk and not fx[i]:
                    di[i] = len([i for i in src(0,m,i,e,pk=m[i]) if m[i] not in '0'+pk])            
            s = min(di,key=lambda n:di[n])
            rp = di[s]
            ct += 10000 * rp
            r2 = src(-2,m,p,-1,pk=pk)
            isDead = len(r2) > 1
        used = []
        for i in range(size):
            if m[i] not in '0x':
                if p == -1:
                    p1 = [j for j in range(size) if j not in used and leaf[j] == m[i]][0]
                    used.append(p1)
                # dst = len(src(0,m,i,p,pk=m[i]))
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p,sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    put = lambda cur:q.put((g[cur] + heu(cur),cur)) if n > 0 else q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.popleft()
    put(cur)
    while 1:
        if n == -4 and not q:
            return -1
        if n == -2 and len(q) > 1:      # default
            break
        if n == -1 and not q:      # default
            return mkd
        cur = get()
        if n == -3 and m[cur] != '0' and cur not in li:
            break
        if n in [-4,0] and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur,pk):
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

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [[4,4],[4,5],[5,5]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        fix, = a
        fxli(fix,1)
        di = {}
        for i in range(16):
            y,x = divmod(i,4)
            li = [m[i] for i in range(16) if (i // 4 == y or i % 4 == x) and fx[i]]
            if len(li) == 2:
                di[i] = '1' if '1' not in li else '2' if '2' not in li else '3'
        leaf = ''.join([m[i] if fx[i] else di[i] if i in di else '0' for i in range(16)])
        di = {(0,5,10):[[6,1],2,6,[9,4],8,9],(3,6,9):[[5,2],1,5,[10,7],11,10],
              (6,9,12):[[5,8],4,5,[10,13],14,10],(5,10,15):[[6,11],7,6,[9,14],13,9],
              (3,5,10):[6,2,1,0,7,11],(5,10,12):[9,13,14,15,8,4],
              (0,6,9):[5,1,2,3,4,8],(6,9,15):[10,14,13,12,11,7]}
        tp = tuple(sorted(fix))
        if tp in di:
            li = di[tp]
        else:
            li = []
            while len(li) < 6:
                p = min([i for i in range(16) if not fx[i]],key=lambda n:len(exp(0,m,n)))
                li.append(p)
                fx[p] = 1
            fxli(li,0)
    if t == 1:
        leaf = ['x' if i == 'x' else '0' for i in m]
        leaf[6:9] = '123'
        leaf[11:14] = '456'
        leaf = ''.join(leaf)
        li = [i for i in range(20) if i not in [6,7,8,11,12,13] and m[i] != 'x'][:6]
    if t == 2:
        global hli
        leaf,hli, = a
        li = [i for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14] if i not in hli]
    hd,hdr = [],{}
    leaf1 = list(leaf[:])
    for i in li:
        b = t == 0 and type(i) == list
        if b:
            j,i = i
        pk = leaf1[i]
        if pk == '0':
            if t == 2:
                di = {}
                for pk in '12345678':
                    if pk in [m[i] for i in hd]:
                        continue
                    r = src(-4,leaf1,i,leaf1.index(pk),hd,pk = pk)
                    if r != -1:
                        break
                else:
                    m = src(1,m,leaf,i,'0')                    
                    fx[i] = 1
                    continue
            else:
                r = src(-3,leaf1,i,-1,hd)
            pk = leaf1[r[-1]]
            hd.append(i)
            hdr[i] = r
            leaf1[r[-1]],leaf1[i] = '0',pk
        if b:
            m = src(1,m,''.join(leaf1),j,pk)
        m = src(1,m,''.join(leaf1),i,pk)
        fx[i] = 1
    m = src(1,m,''.join(leaf1),-1,-1)
    for i in hd[::-1]:
        res.append([hdr[i],int(m[i])])
    return res

if __name__ == '__main__':

    # t,m,a = 0,'0200311022303001',[15, 9, 4]
    t,m,a = 0,'2203301001012030',[9, 12, 3]
    t,m = 1,'xx00xx54300261xx0xxx'
    t,m1,m2,a = 2,'0207000003040008005060010','0052004008000107030000600',[12,21]

    ts = time()
    res = main(t,m,a) if t == 0 else main(t,m) if t == 1 else main(t,m1,m2,a)
    te = time() - ts
    print(res)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
