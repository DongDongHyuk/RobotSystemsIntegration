from time import time
from Tool.Printer import *

def exc(m,s,e,li=-1):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    r = [e,s] if li == -1 else li
    info = [r,int(m[s])]
    return [''.join(m),info]

def aro(p):
    dxy = [-sx,1,sx,-1]
    li = [[(0,1,2,3),(3,7,11,15),(12,13,14,15),(0,4,8,12)],[],[]][t]
    return [p + dxy[i] for i in range(4) if p not in li[i]]

def exp(n,m,p=-1):
    res = []
    for i in range(size) if n > 0 else [p]:
        if (n > 0 and m[i] != '0') or fx[i]:        # default
            continue
        if t == 0 and n > 0 and i in hli:       # A
            continue
        for j in aro(i):
            if t == 0 and j in hli:        # A
                isg = j == hli[0]
                li = [k for k in aro(j) if k not in hli+[i] and (abs(i-j) == abs(j-k) == (1 if isg else 4))]
                if not li:
                    continue
                j = li[0]
            if m[j] in ['x','0x'][n > 0] or fx[j]:        # default
                continue
            res.append(exc(m,i,j) if n > 0 else [j,j])
    return res

def src(n,m,*a):
    global res
    if n < 1:
        s,e = a
        li = []         # temp (n == -3)
    if n == 1:
        p,pk = a
    if n == 2:
        leaf,ct = a
    q = [m if n > 0 else s] 
    mkd = {i:[] for i in q}
    while 1:
        if n == -3 and not q:       # temp
            return li
        if n == -2 and len(q) > 1:
            break
        cur = q.pop(0)
        if n == -1 and m[cur] not in e + ['0']:        # A
            break
        if n == 0 and cur == e:
            break
        if n == 1:
            if (pk == -1 and cur == p) or (pk != -1 and cur[p] == pk):
                break
        if n == 2 and len([i for i in range(16) if cur[i] not in '0x' and cur[i] == leaf[i]]) >= ct:        # A
            break
        for i,j in exp(n,cur if n > 0 else m,cur):
            if i not in mkd:
                if n == -3:
                    li.append(i)
                q.append(i)
                mkd[i] = mkd[cur] + [j]
    path = mkd[cur]
    if n > 0:
        res += path
        return cur
    return path
    
def sort(m,p,pk):
    Max = 0
    while 1:
        try:
            hd = [p]+src(-2,m,p,-1)
            hd = hd[:-1]
            n = Max - len([i for i in fx if fx[i]])
            hd = hd[:n]
            for i in hd:
                m = src(1,m,i,'0')
                fx[i]=1
            fxli(hd,0)
            r = src(0,m,m.index(pk),p)
            fxli(hd,1)
            for i in r:
                if i in hd:
                    fx[i]=0
                m = src(1,m,i,pk)
        except:
            print(Max)
            fxli(hd,0)
            Max -= 1
        else:
            break
    fx[p] = 1
    return m

def main(g_t,m,*a):
    global t,sy,sx,size,fx,fxli,res 
    t = g_t
    sy,sx = [[4,4],[None,None],[None,None]][t]
    size = sy * sx
    fx = {i:0 for i in range(size)}
    fxli = lambda li,n: fx.update({i:n for i in li})
    res = []
    if t == 0:
        global hli
        leaf,hli = a
        tile = [[0,1,4,5],[3,2,7,6],[12,8,13,9],[15,11,14,10]]
        x = [i for i in tile if [j for j in i if m[j] == 'x']]
        h = [i for i in tile if [j for j in i  if j in hli]]
        li = [i for i in range(4) if tile[i] not in x + h]
        di1 = {'03','12'}
        di2 = {'01':1,'02':4,'13':7,'23':13}
        if len(li) == 2:
            seq = [tile[i][0] for i in li]
            st = ''.join(map(str,li))
            if st in di1:
                if len(h) == 1:
                    if not [i for i in aro(h[0][0]) if i not in hli]:                        
                        seq.append(h[0][0])
                    else:
                        li = [[len(exp(0,m,i)),i] for i in h[0] if i not in hli]
                        seq.append(min(li)[1])
                else:
                    li = [i for i in h if i in x][0]
                    seq += [i for i in li if i not in hli and m[i] != 'x']
            else:
                seq.append(di2[st])
        else:
            p = x[0][0]
            h1,h2 = hli
            side = [[0,4,8,12],[3,7,11,15],[0,1,2,3],[12,13,14,15]]
            g,s = [i for i in side[:2] if h1 in i],[i for i in side[2:] if h2 in i]
            st = ''.join(map(str,[i for i in range(4) if h1 in tile[i] or h2 in tile[i]]))
            if g and s and st in di2:
                li = [[len(exp(0,m,i)),i] for i in set(g[0]+s[0]) if i not in hli+x[0]]
                seq = [i[1] for i in sorted(li)][:3]
            else:
                li = []
                for i in x[0][1:]:
                    if m[p] == 'x':
                        ct = len(aro(i)) - len(exp(0,m,i))
                        li.append([ct,i])
                    else:
                        a,b = len(exp(0,m,i)),len(exp(0,m,p))
                        if a == 1 or a < b :
                            li.append([a,i])
                if li:
                    p = max(li)[1]
                seq = [p] +[i for i in x[0] if m[i] != 'x' and i != p]
        hd,hdr = [],{}
        leaf1 = list(leaf[:])
        for i in seq:
            pk = leaf1[i]
            if pk == 'x' or i in hli or fx[i]:
                continue
            if pk == '0':
                r = [i]+src(-1,leaf1,i,hd)
                pk = leaf1[r[-1]]
                hd.append(pk)
                hdr[pk] = r
                leaf1[r[-1]],leaf1[i] = '0',pk
            m = sort(m,i,pk)
        for i in range(9):
            m = src(2,m,''.join(leaf1),i)
        for i in hd[::-1]:
            res.append([hdr[i],int(i)])
    return res

if __name__ == '__main__':

    # t,m1,m2,hli = 0,'07001x0002534068','07004x1000630258',[2,7]

    # 모든 홀이 고정 팩일때
    # t,m1,m2,hli = 0,'28007x0153060400','12003x0060470850',[12, 2]       # dart 14m 50s
    t,m1,m2,hli = 0,'106504x000037208','608000x005123470',[8, 1]
    
    
    ts = time()    
    res = main(t,m1,m2,hli)
    te = time() - ts
    # for i in res:
    #     prt(i,4,4)
    print(res)
    print("{}step, idle {}s(DART-Studio {}m {}s) \n".format(len(res),round(te,3),int((te*250)//60),int((te*250)%60)))
