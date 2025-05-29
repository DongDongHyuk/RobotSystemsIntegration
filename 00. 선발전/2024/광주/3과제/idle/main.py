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
    def put(cur):
        if n > 0:
            q.put((g[cur] + heu0(cur), cur))
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
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                mkd[i] = mkd[cur] + [j]
                g[i] = g[cur] + 1
                put(i)
    res1 = mkd[cur]
    if n > 0:
        if n != 2:
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
        leaf = ['0']*18
        def gs(p):
            y1,x1 = (p//3)%3,p%3
            li = []
            for i in (range(9) if p < 9 else range(9,18)):
                y2,x2 = ((i//3) % 3),i%3
                if (y1 == y2 or x1 == x2) and (y1 < y2 or x1 < x2):
                    li.append(i)
            return [leaf[i] for i in li if leaf[i] != '0']
        b1 = lambda p:(p < 9 or leaf[p-9] != '0')
        b2 = lambda p:(p > 8 or leaf[p+9] == '0')
        di1 = {6:[6,3,0],7:[7,4,1],8:[8,5,2],15:[15,12,9],16:[16,13,10],17:[17,14,11]}
        di2 = {8:[8,7,6],5:[5,4,3],2:[2,1,0],17:[17,16,15],14:[14,13,12],11:[11,10,9]}
        notUse = [i for i in range(18) if v1[i%9] == '0']
        for p in range(9):
            if v1[p] == '3':
                leaf[p],leaf[p+9] = '1','2'
        for i in range(6):
            p = [6,7,8,15,16,17][i]
            line = di1[p]
            li = [i for i in line if leaf[i] != '0']
            pk = '0'
            if li:
                pk = leaf[li[0]]
                # notUse += line[:line.index(li[0])]
            pk1 = v2[i]
            if pk1 != pk:
                li1 = []
                for j in di1[p]:
                    if leaf[j] == '0':
                        if v1[j%9] == pk1:
                            li1.append(j)
                            break
                        notUse.append(j)
                leaf[li1[0]] = pk1
        for i in range(6):
            p = [8,5,2,17,14,11][i]
            line = di2[p]
            li = [i for i in line if leaf[i] != '0']
            pk = '0'
            if li:
                pk = leaf[li[0]]
                # notUse += line[:line.index(li[0])]
            pk1 = v3[i]
            if pk1 != pk:
                li1 = []
                for j in di2[p]:
                    if leaf[j] == '0':
                        if v1[j%9] == pk1:
                            li1.append(j)
                            break
                        notUse.append(j)
                leaf[li1[0]] = pk1

        for i in range(9):
            pk1,pk2 = leaf[i],leaf[i+9]
            if pk1 == '0' and pk2 != '0':
                for pk in '12':
                    if leaf.count(pk) == 6 or (v1[i] == '2' and pk == '1'):
                        continue
                    leaf[i] = pk
                    break

        # 남는팩 추가 

        print([i for i in range(18) if leaf[i] == '0' and i not in notUse],'\n')
        print(v1[0:3])
        print(v1[3:6])
        print(v1[6:9],'\n')
        print(v2[3:])
        print(v2[:3],'\n')
        print(v3[3:])
        print(v3[:3],'\n')
        prt(''.join(leaf),3,3,2)
        exit()

        leaf = ''.join(leaf)

        for i in range(9):
            if leaf[i] != '0':
                m = src(1,m,-1,i,leaf[i])
                fx[i] = 1         
        src(1,m,leaf,-1,-1)
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
    # t,m,v1,v2,v3 = 1,'111002221120002201','120133302','112222','212222'
    # t,m,v1,v2,v3 = 1,'212111202010102002','102233021','221121','112121'
    # t,m,v1,v2,v3 = 1,'112122120002120100','301321202','222202','211211'
    # t,m,v1,v2,v3 = 1,'210121021020221001','023131222','222121','211012'
    # t,m,v1,v2,v3 = 1,'112111122020220000','211032302','112222','221221'
    # t,m1,m2 = 2,'103005x008026470','850001x427600030'

    ts = time()
    res = main(t,m) if t == 0 else main(t,m,v1,v2,v3) if t == 1 else main(t,m1,m2)
    te = time() - ts
    print(res)
    print('visited :',vs)
    # for i in res:
    #     print(i)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))

