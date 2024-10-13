from collections import deque
from time import time
from printer import printf

def exc(m,s,e,li=[]):
    global ing
    m = list(m)
    m[s],m[e] = m[e],m[s]
    step = li if li else [e,s]
    pack = 10 if m[s] == 'a' else int(m[s])
    info = ([ing] if t == 2 else []) + [step,pack]
    return [''.join(m),info]
    
def aro(pos):
    if t == 0:
        di = {7:[2,6,8,11,13,17],
        11:[6,7,10,13,16,17],12:[],13:[7,8,11,14,17,18],
        17:[7,11,13,16,18,22]}
        if pos in di:
            return di[pos]
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

def exp(n,m,pos=-1):
    res = []
    for i in range(size) if n > 0 else [pos]:       
        if ((n > 0 or n == -1) and m[i] != '0') or i in fix:
            continue        
        for j in [j for j in aro(i) if m[j] not in ['x','0x'][n > 0] and j not in fix]:            
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def bfs(n,m,*a):
    global res
    if n == -1:
        s, = a
    if n == 0:
        s,e = a
    if n == 1:
        leaf,pos,pack = a
    cur = m if n > 0 else s
    que = deque([cur])
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.popleft()
        if n == -1 and m[cur] != '0':
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pos == -1 and cur == leaf) or (pos != -1 and cur[pos] == pack):
                break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [step[cur]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append(step[cur])
    if n > 0:
        res += path[::-1][1:]
        return mkd[-2]
    return path[::-1][1:]
    
def sort(m,leaf,pos,pack):
    global fix
    hold = []
    if len(exp(0,m,pos)) == 1:
        m = bfs(1,m,leaf,pos,'0')
        hold.append(pos)
    r = bfs(0,m,m.index(pack),pos)
    fix += hold
    for i in r:
        if i in hold:
            fix.remove(i)
        m = bfs(1,m,leaf,i,pack)
    fix.append(pos)
    return m

def main(g_t,m,*a):    
    global t,sy,sx,size,fix,res,cache
    t = g_t
    sy,sx = [[5,5],[4,4],[4,4]][t]
    size = sy * sx
    fix = []
    res = []
    cache = {}      # cache reset
    if t == 0:
        leaf = '1x0x23000450006700089x0xa'
        fix = [2,22]
        for i in [0,24,4,20,5,19,15,9,10,14]:
            m = sort(m,leaf,i,leaf[i])
    if t == 1:
        leaf = list('1234567800000000')
        leaf[m.index('x')] = 'x'
        leaf = ''.join(leaf)
        for i in [1,2,0,3,5,6,4,7]:
            m = sort(m,leaf,i,leaf[i])
    if t == 2:
        global ing
        ing = 0
        m1 = m[:]
        m2,leaf1 = a
        leaf2 = ''.join([leaf1[0+i:4+i][::-1] for i in range(0,16,4)])
        for i in range(2): 
            ing = i
            fix = []
            m = [m1,m2][i][:]
            leaf = [leaf1,leaf2][i][:]
            leafc = leaf[:]
            li = {5:[15,11,14,13],6:[12,8,13,14],9:[3,7,2,1],10:[0,4,1,2]}[m.index('x')]
            hold = {}
            unhold = []
            for i in li:
                pack = leafc[i]
                if i in hold or pack == '0':
                    r = bfs(-1,leafc,i)
                    pos = r[-1]
                    pack = leafc[pos]
                    hold[pack] = [i]+r
                    unhold.append(pack)
                    leafc = list(leafc)
                    leafc[pos] = '0'
                    leafc = ''.join(leafc)
                m = sort(m,leaf,i,pack)
            pack, = [i for i in leaf if i not in '0x' and m.index(i) not in fix]
            m = sort(m,leaf,leaf.index(pack),pack)
            for pack in unhold[::-1]:
                r = hold[pack]            
                m,step = exc(m,r[-1],r[0],r)
                res.append(step)
    return res

if __name__ == '__main__':

    t,m = 0,'5x0x3400089000a600012x0x7'
    # t,m = 1,'0000050087x16342'
    # t,m1,m2,leaf = 2,'10300x0402000005','000042x513000000','000000x050004321'
        
    ts = time()    
    res = main(t,m) if t < 2 else main(t,m1,m2,leaf)
    te = time() - ts
    print(res)
    print("{}step, idle {}s(dart {}m {}s) \n".
    format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))


