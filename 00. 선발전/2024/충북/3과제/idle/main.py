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
            if t == 0 and n > 0 and j in hli:
                continue
            res.append(exc(m,j,i,di[j]) if n > 0 else [j,j])        
    return res

mkdCt = 0
def src(n,m,*a):
    global res,mkdCt
    if n < 1:
        s,e = a
        if n == 0 and (s,e) in cache:
            return cache[(s,e)]
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = PriorityQueue() if n > 0 else []
    mkd = {cur:[cur]}
    g = {cur:0}
    def heu(m):
        ct = 0
        if p != -1:
            s,e = m.index(pk),leaf.index(pk)
            r1 = src(0,m,s,e)
            ct += len(r1)
            ct += 10 * len([i for i in r1 if m[i] not in '0'+pk])
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
            # if isDead:
            #     for i in range(len(r2)-1,-1,-1):
            #         i = r2[i]
            #         if m[i] not in '0':
            #             ct += 10000 * len(src(0,m,i,p))
            # li = [i in r2 and m[i] not in '0'+pk for i in r1[1:]]
            # if isDead and li and any(li):
            #     ct += 100
        for i in range(size):
            if m[i] not in '0x':
                # 길찾기 ver
                dst = len(src(0,m,i,leaf.index(m[i]) if p == -1 else p))
                 
                # 맨해튼 ver
                # y1,x1 = divmod(i,sx)
                # y2,x2 = divmod(leaf.index(m[i]) if p == -1 else p,sx)
                # dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                
                ct += (dst if p == -1 else (1000 * (size - dst) if isDead and i in r2 else -dst))

        if p != -1 and p in src(-1,m,s,-1):
            ct = -99999 * (2 if m[p] == pk else 1)

        # print('ct ->',ct)
        # print(p,pk)
        # prt(m,5,5)
        # input()

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
        if n == -3 and m[cur] not in e + ['0']:
            break
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
    if n == 0:
        cache[(s,e)] = res1
    return res1

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [5,5]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        global hli
        leaf,hli = a
        li = [[0,5,10,15,20,1,6,11,16,21,],[4,9,14,19,24,3,8,13,18,23]]
        li = min(li,key = lambda li:[m[i] for i in li].count('x'))
        for i,j in [[0,5],[5,10]]:
            li[i:j] = sorted(li[i:j],key = lambda i:len(exp(0,m,i)))
        li = [i for i in li+[2,7,12,17,22] if len(exp(0,m,i)) == 1] + li
    if t == 2:
        hli = []
        leaf = list(m)
        m = '1234567800000000000000000'
        ct = 1
        for i in range(25):
            pk = leaf[i]
            if pk == 'x':
                leaf[i] = '0'
            elif pk != '0':
                leaf[i] = str(ct)
                ct += 1
        leaf = ''.join(leaf)
        li = [20,21,22,23,24]
    hd,hdr = [],{}
    leaf1 = list(leaf[:])
    for i in li:
        if len([i for i in fx if fx[i] if m[i] != '0']) > 5:
            break
        if m[i] == 'x' or i in hli or fx[i]:
            continue
        fxli([i for i in hli if len(exp(0,m,i)) == 1],1)
        pk = leaf1[i]
        if pk == '0':
            r = src(-3,leaf1,i,hd)
            pk = leaf1[r[-1]]
            hd.append(pk)
            hdr[pk] = r
            leaf1[r[-1]],leaf1[i] = '0',pk            
        m = src(1,m,''.join(leaf1),i,pk)
        fx[i] = 1
    m = src(1,m,''.join(leaf1),-1,-1)
    for i in hd[::-1]:
            res.append([hdr[i],int(i)])
    return res

if __name__ == '__main__':

    t,m1,m2,hli = 0,'3040500x6070800000x102000','0700000x8005006004x030201',[6, 13, 16]
    t,m = 2,'0700000x8005006004x030201'

    ts = time()
    res = main(t,m1,m2,hli) if t == 0 else main(t,m)
    te = time() - ts
    print(res)
    # for i in res:
    #     print(i)
    print('visited :',mkdCt)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

