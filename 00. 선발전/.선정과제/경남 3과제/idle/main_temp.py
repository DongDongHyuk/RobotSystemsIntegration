from queue import PriorityQueue
from collections import deque

def exc1(m,s,e,r):
    m=list(m)
    m[s],m[e]=m[e],m[s]
    pk=int(m[s])
    if t==1:
        info=[[1,r[0],int(m[s])],
              [1,r[1],int(m[e])],
              [0,r[1],int(m[s])],
              [0,r[0],int(m[e])]]
    else:
        info=[r,pk]
    return [''.join(m),info]

def aro(pos):
    if pos in cache:
        return cache[pos]
    res=[]
    dy,dx=[-1,0,1,0],[0,1,0,-1]
    y,x=divmod(pos,sx)
    for i in range(4):
        ny,nx=y+dy[i],x+dx[i]
        if -1<ny<sy and -1<nx<sx:
            res.append(ny*sx+nx)
    cache[pos]=res
    return cache[pos]

def exp(n,m,p=-1):
    res=[]
    di1,di2={},{}
    for i in range(si):
        if not fx[i] and m[i]!='x':
            if m[i]!='0' or n<1:
                di1[i]=i
            if m[i]=='0' or n<1 or t==1:
                di2[i]=i
            
    for i in di1 if n>0 else [p]:
        if n==-2 and m[i]!='0':
            continue
        q=deque([i])
        r={i:[di1[i]]}
        while q:
            cur=q.popleft()
            for j in [(i+j)%8 for j in [-3,-2,-1,1,2,3]] if t==1 else aro(cur):
                if j in r or j not in di2:
                    continue
                if t==1:
                    if i==j:
                        continue
                    if m[i] in Pk1 and m[j] in Pk1:
                        continue
                    if m[i] in Pk2 and m[j] in Pk2:
                        continue
                if n>0:
                    q.append(j)
                r[j]=r[cur]+[di2[j]]
                res.append(exc1(m,di2[j],di1[i],r[j]) if n>0 else [j,j])
    return res
    
vs=0
def src(n,m,*a):
    global res,vs
    if n<1:
        s,e=a
        if n in [0,-1] and (n,s,e) in cache:
            return cache[n,s,e]
    if n in [1,2]:
        leaf,p,pk=a
    cur=m if n>0 else s
    q=PriorityQueue() if n>0 else deque([])
    mkd,g={cur:[cur]},{cur:0}
    def h1(m):
        ct=0
        if p!=-1:
            r1=src(0,m,m.index(pk),p)[1:]
            ct+=len(r1)
            ct+=100*len([i for i in r1 if m[i] not in '0'+pk])
            r2=src(-1,m,p,-1)
            if len(r2)>1:
                if m[r2[1]]==pk and m[r2[0]]!='0':
                    ct+=10000
        else:
            for i in range(si):
                if not fx[i] and m[i] not in '0x':
                    y1,x1=divmod(i,sx)
                    y2,x2=divmod(leaf.index(m[i]),sx)
                    ct+=abs(y1-y2)+abs(x1-x2)
        return ct
    def h2(m):
        ct=0
        li=[0,1,2,3,4,5,6,7]
        for pk in Pk1+Pk2:
            p2=leaf.index(pk)
            if pk in m:
                p1=m.index(pk)
                if 'x' in m:
                    n=m.index('x')-leaf.index('x')
                    if p1==(p2+n)%8:
                        ct-=10000
                else:
                    n1,n2=li.index(p1),li.index(p2)
                    st1=[m[i] for i in li[n1:]+li[:n1]]
                    st2=[leaf[i] for i in li[n2:]+li[:n2]]
                    for i in range(len(st1)):
                        if st1[i]==st2[i]:
                            ct-=10000
            else:
                ct-=100
        return ct
    def put(cur):
        q.put((g[cur]+(h2 if n==2 else h1)(cur), cur)) if n>0 else q.append(cur)
    def get():
        return q.get()[1] if n>0 else q.popleft()
    put(cur)
    while 1:
        if n==-1 and len(q)>1:
            break
        cur=get()
        if n>0:
            vs+=1
        if n==-2 and m[cur]!='0' and cur not in e:
            break
        if n==0 and cur==e:
            break
        if n==1:
            if (p==-1 and cur==leaf) or (p!=-1 and cur[p]==pk):
                break
        if n==2:
            h=h2(cur)
            if 'x' in cur and h==-10000*len(Pk1+Pk2):
                break
            if 'x' not in cur and h==-10000*8*(8-Ct):
                break
        for i,j in exp(n,cur if n>0 else m,cur):
            if i not in mkd:
                mkd[i],g[i]=mkd[cur]+[j],g[cur]+1
                put(i)
    res1=mkd[cur]
    if n>0:
        res+=res1[1:]
        return cur
    if n in [0,-1]:
        cache[n,s,e]=res1
    return res1
    
def main(g_t,m,*a):
    global t,sy,sx,si,fx,fxli,cache,res
    t=g_t
    sy,sx=[1,8] if t==1 else [3,4]
    si=sy*sx
    fx={i:0 for i in range(si)}
    fxli=lambda li,n:fx.update({i:n for i in li})
    cache={}
    res=[]
    if t==0:
        global hli
        leaf,hli=a
        xli=[i for i in range(si) if m[i]=='x']
        li=[0,3,8,11]
        if xli:
            x=xli[0]
            li=[[4,8],[0,4,8],[3,7,11],[7,11],
                [0,8],[4,0,8],[7,3,11],[3,11],
                [4,0],[8,4,0],[11,7,3],[7,3]][x]
        seq=[i for i in li if i not in xli+hli]
        if not xli:
            seq=seq[:len([i for i in m if i!='0'])-5]
        hd,hdr=[],{}
        leaf1=list(leaf)
        for i in seq:
            pk=leaf1[i]
            if pk=='0':
                r=src(-2,leaf1,i,hd)
                pk=leaf1[r[-1]]
                hd.append(i)
                hdr[i]=r
                leaf1[r[-1]],leaf1[i]='0',pk
            m=src(1,m,''.join(leaf1),i,pk)
            fx[i]=1
        m=src(1,m,''.join(leaf1),-1,-1)
        for i in hd[::-1]:
            res.append([hdr[i],int(m[i])])
    if t==1:
        global Ct,Pk1,Pk2
        leaf,=a
        st=[i for i in '12345678' if i in leaf]
        Ct=leaf.count('0')
        Pk1,Pk2=st[:-4],st[-4:]
        
        # temp
        #for i,j in exp(1,m):
            #tl(i)
            #tl(j)
        #exit()
        
        src(2,m,leaf,-1,-1)
    return res