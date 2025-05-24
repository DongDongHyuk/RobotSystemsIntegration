from time import time
from Tool.Printer import *
from queue import *

def exc(m,s,e,r):
    m = list(m)
    m[s],m[e] = '2' if m[e] == '1' else '1','0'
    info = [r,int(m[s])]
    return [''.join(m),info]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [-1,-1,-1,0,1,1,1,0],[-1,0,1,1,1,0,-1,-1]
    y,x = divmod(pos,sx)
    for i in range(8):
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
        for j in aro(i):
            if fx[j] or m[j] == 'x' or m[j] != '0':
                continue
            if t == 0:
                dire = abs(j-i)
                if (dire in [1,4] and m[i] != '1') or (dire in [3,5] and m[i] != '2'):
                    continue
            res.append(exc(m,j,i,[i,j]) if n > 0 else [j,j])        
    return res

def src(n,m,*a):
    global res
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
        ct -= 100 * len([i for i in range(16) if leaf[i] != '0' and m[i] == leaf[i]])
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
    global t,sy,sx,size,fx,fxli,cache,res
    t = g_t
    sy,sx = [[4,4],[None,None],[None,None]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        leaf,=a
        src(1,m,leaf,-1,-1)

    return res

if __name__ == '__main__':

    t,m1,m2 = 0,'1111121111210000','0102''2122''0211''2011'

    ts = time()
    res = main(t,m1,m2)
    te = time() - ts
    print(res)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

