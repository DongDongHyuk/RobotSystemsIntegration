from time import time
from printer import prt

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    info = [[e,s] if li == -1 else li,int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [(0,1,2,3,4),(4,9,14,19,24),(20,21,22,23,24),(0,5,10,15,20)]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if n == -99 and i not in hli:       # 홀 처리
            continue
        if t == 0 and n > 0 and i in hli:         # 홀 처리
            continue
        li = aro(i)
        di = {}        # 홀 처리
        for j in li:
            if t == 0 and n > 0 and j in hli:
                for k,v in bfs(-99,m,j).items():
                    if k not in li + hli + [i,j]:
                        di[k] = v[::-1] + [j,i]
        li += list(di)
        for j in li:
            if m[j] in ('0x' if n > 0 else 'x') or j in fix:
                continue
            res.append(exc(m,i,j,di[j] if j in di else -1) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n < 0:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,p,pk = a
    cur = m if n > 0 else s
    q = [cur]
    mkd = {cur:[]}
    while 1:
        if n == -99 and not q:        # 홀 처리
            return mkd
        cur = q.pop(0)
        if n == -1 and m[cur] != '0':
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                q.append(i)
                mkd[i] = mkd[cur] + [i]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    r = bfs(0,m,m.index(pk),p)
    for i in r:
        m = bfs(1,m,-1,i,pk)
    fix.append(p)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res
    t = g_t
    sy,sx = [[5,5],[0,0],[0,0]][t]
    size = sy * sx
    fix = []
    res = []
    if t == 0:
        global hli
        leaf,hli = a

        # temp
        print('root')
        prt(m,5,5,hli)
        print('leaf')
        prt(leaf,5,5,hli)

        for i,j in exp(1,m):
            print('step ->', j)
            prt(i,5,5,hli)

    return res

# t,m,leaf,a = 0,'3040500x6070800000x102000','0700000x8005006004x030201',[6,13,16]

m = [0,0,0,0,0,
     0,1,0,0,0,
     0,0,0,0,0,
     0,0,0,0,0,
     0,0,0,0,0]
t,m,leaf,a = 0,list(map(str,m)),list(map(str,m)),[11,12,13]

ts = time()    
res = main(t,m,leaf,a) if t == 0 else None
te = time() - ts
print(res)
print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))