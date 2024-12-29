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

def hexp(m,i):         # expand Hole
    if i in ca:
        return ca[i]
    li = aro(i)
    di = {}
    for j in li:
        if j in hli:
            for k,v in bfs(-99,m,j).items():
                if k not in li + hli + [i,j]:
                    di[k] = v[::-1] + [j,i]
    ca[i] = di
    return di

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or i in fix:
            continue
        if n == -99 and i not in hli:       # 홀 처리
            continue
        li = aro(i)
        if t == 0 and n > 0:        # 홀 처리
            if i in hli:
                continue            
            di = hexp(m,i)
            li += list(di)
        for j in li:
            if m[j] in ('0x' if n > 0 else 'x') or j in fix:
                continue
            res.append(exc(m,i,j,di[j] if j in di else -1) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == -99:
        s, = a
    if n == -1:
        s,li = a
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
        if n == -1 and m[cur] not in ['0'] + li:
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (p == -1 and cur == leaf) or (p != -1 and cur[p] == pk):
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
    if m[p] != pk:
        b = len(exp(0,m,p)) == 1
        if b:
            m = bfs(1,m,-1,p,'0')
        r = bfs(0,m,m.index(pk),p)
        if b:
            fix.append(p)
        for i in r:
            if i in hli:
                continue
            if i in fix:
                fix.remove(i)
            m = bfs(1,m,-1,i,pk)
    fix.append(p)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,ca
    t = g_t
    sy,sx = 5,5
    size = sy * sx
    fix = []
    res = []
    ca = {}
    if t == 0:
        global hli
        leaf,hli = a
        xli = [i for i in range(25) if m[i] == 'x']
        ct = 0
        li = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
              [4,9,14,19,24,3,8,13,18,23,2,7,12,17,22],
              [20,21,22,23,24,15,16,17,18,19,10,11,12,13,14],
              [0,5,10,15,20,1,6,11,16,21,2,7,12,17,22]]
        di = {len([j for j in i if j in xli]):i for i in li}
        li = di[min(di)]
        rs = {}
        hold = []
        m1 = leaf[::]
        for i in range(15):
            if i in [0,5]:
                j = li[i + 4]
                if m[li[9]] == 'x' or m[li[14]] == 'x':
                    pk = m1[j]
                    if pk == '0':
                        m = bfs(1,m,m1,j,pk)
                        fix.append(j)
                    else:
                        m = sort(m,j,pk)
            i = li[i]
            if i in fix + hli: 
                continue
            if len([i for i in fix if m[i] != '0']) == 7:
                break
            pk = m1[i]
            if pk == '0':
                r = [i] + bfs(-1,m1,i,hold)
                pk = m1[r[-1]]
                hold.append(pk)
                rs[pk] = r
                m1 = exc(m1,i,r[-1])[0]
            m = sort(m,i,pk)
        m = bfs(1,m,m1,-1,-1)
        for i in hold[::-1]:
            r = rs[i]
            m,step = exc(m,r[-1],r[0],r)
            res.append(step)

    return res

if __name__ == '__main__':
    t,m,leaf,a = 0,'3040500x6070800000x102000','0700000x8005006004x030201',[6,13,16]
    t,m,leaf,a = 0,'000x806700000000x14530020','000x615273040008x00000000',[14, 13, 0]

    ts = time()    
    res = main(t,m,leaf,a) if t == 0 else None
    te = time() - ts
    print(res)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*300)//60),int((te*300)%60)))
