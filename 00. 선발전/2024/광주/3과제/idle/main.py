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
    di1,di2 = {},{}
    for i in range(18 if t == 1 else si):
        if m[i] != '0':
            di1[i%si] = i
        if m[i] == '0' and i%9 not in di2:
            di2[i%si] = i
    
    for i in di1 if n > 0 else [p%si]:
        if fx[di1[i] if n > 0 else p] or m[i] == 'x':
            continue
        if n == -3 and m[i] != '0':
            continue
        
        di = src(-1,m,di1[i],-1) if n > 0 else aro(i)

        for j in di:
            if fx[j] or m[j] == 'x' or (n == -1 and j not in di2):
                continue
            res.append(exc(m,di2[j%si],di1[i],di[j]) if n > 0 else [di2[j]]*2)
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
        used = []
        for i in range(size*sz):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                p1 = p if p != -1 else [j for j in range(size*sz) if leaf[j] == m[i] and j not in used][0]
                used.append(p1)
                y2,x2 = divmod(p1,sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst ** 2
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)
        return ct
    def heu1(m):
        ct1,ct2 = 0,0
        di = {'00':0,'10':1,'11':1,'21':1,'20':2,'22':2,'12':3}
        for i in range(9):
            if str(di[m[i]+m[i+9]]) == v1[i]:
                ct1 += 1
            ct2 += -10000 * (v1[i] == '2' and m[i] == '2')
            ct2 += -10000 * (v1[i] == '3' and m[i] == '1')
        li1 = [[0,3,6],[1,4,7],[2,5,8],[9,12,15],[10,13,16],[11,14,17]]
        for i in range(6):
            pk = '0'
            for j in li1[i]:
                if m[j] != '0':
                    pk = m[j]
            if pk == v2[i]:
                ct1 += 1
        li1 = [[6,7,8],[3,4,5],[0,1,2],[15,16,17],[12,13,14],[9,10,11]]
        for i in range(6):
            pk = '0'
            for j in li1[i]:
                if m[j] != '0':
                    pk = m[j]
            if pk == v3[i]:
                ct1 += 1
        return [ct1 == 21,0] # ((-100 * ct1) + ct2)]        # temp
    def put(cur):
        if n > 0:
            h = heu1(cur)[1] if n == 2 else heu0(cur)
            q.put((g[cur] + h, cur))
        else:
            q.append(cur)
    get = lambda : q.get()[1] if n > 0 else q.pop(0)
    put(cur)
    while 1:
        if n == -2 and len(q) > 1:      # default
            break
        if n == -1 and not q:      # default
            del mkd[s]
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
    global t,sy,sx,si,fx,fxli,cache,res
    t = g_t
    sy,sx = [3,3] if t == 0 else [3,3] if t == 1 else [4,4]
    si = sy * sx
    fx = {i:0 for i in range(18 if t == 1 else si)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    cache = {}
    res = []
    if t == 0:
        leaf = '123456700'
        src(1,m,leaf,-1,-1)
    if t == 1:
        global v1,v2,v3,ctp
        v1,v2,v3 = a

        # print(src(-1,m,10,-1))      # temp

        prt(m,3,3,2)
        for i,j in exp(1,m):
            print(j)
            prt(i,3,3,2)
        exit()
        # prt('110121112000022022',3,3,2)
        # input()

        # src(2,m)

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
    t,m,v1,v2,v3 = 1,'112202101210200201','110123132','112022','211220'
    # t,m1,m2 = 2,'103005x008026470','850001x427600030'

    ts = time()
    res = main(t,m) if t == 0 else main(t,m,v1,v2,v3) if t == 1 else main(t,m1,m2)
    te = time() - ts
    print(res)
    print('visited :',vs)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

