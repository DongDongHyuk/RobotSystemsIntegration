from DRCF import *

def run(fpt, target, pos, m, hill, p):

    def chk(y, x, pt):
        return -1 < y < len(pt) // m and -1 < x < m

        
    def chkd(x, nx):
        return x // 6 // 3 == nx // 6 // 3

    moving, bf = {}, {}
    for i in range(len(fpt)):
        if fpt[i] != 99:
            moving[i] = []
            y, x = i // m, i % m
            for k in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                ny, nx = y + k[0], x + k[1]
                if chk(ny, nx, fpt) and fpt[ny * m + nx] != 99:
                    moving[i].append(ny * m + nx)

    def exc(pt, x, nx):
        npt = list(pt)
        npt[x], npt[nx] = npt[nx], npt[x]
        return tuple(npt)

    def bfs(pt, start, end):
        if not (start, end) in bf:
            bf[start, end] = node(pt, start, end)
        return bf[start, end]

    def hust(pt, num, pak, ck=0):
        count = 0
        if num == None:
            if m == 5:
                for i in [4, 10]:
                    if pt[i] == target[i]:
                        count -= 1000
                    else:
                        j = target.index(pt[i])
                        count += (abs(i // m - j // m) + abs(i % m - j % m)) ** 2
            else:
                for i in moving:
                    if 0 < pt[i] < 99:
                        j = target.index(pt[i])
                        count += (abs(i // m - j // m) + abs(i % m - j % m))
        if type(num) == int:
            x = pt.index(pak)
            nx = target.index(pak) if ck else num
            answer = bfs(pt, x, nx)
            if not ck and len(moving[num]) == 1 and pt[num] and len(answer) < 3:
                count += 1000
            prev = 0
            for i in answer:
                if 0 < pt[i] < 99:
                    count += 100
                if prev > 100 and not pt[i] > 100 and ck:
                    break
                prev = pt[i]
            count += len(answer)
        return count

    def end(pt, num, pak, ck=0):
        if num == None:
            return list(pt) == list(target)
        if type(num) == list:
            for i in num:
                if not pt[i]:
                    return False
                if m == 5 and pt[i] in hill[pt[(i//5)*5+2]] and len(num) != 2:
                    return False
            return True
        if type(num) == int:
            if ck:
                return chkd(pt.index(pak), target.index(pak))
            else:
                return pt[num] == pak



    def node(pt, start, end):
        q, prev = deque([start]), {start: -1}
        while q:
            here = q.popleft()
            for nx in moving[here]:
                if nx in prev or pt[nx] == 99:
                    continue
                if not hill and pt[here] == 100 and nx == 4:
                    continue
                if 0 < pt[nx] < 99 and end == None:
                    continue
                if pt[nx] in hill and not pt[start] in hill[pt[nx]]:
                    continue
                q.append(nx)
                prev[nx] = here
                if nx == end:
                    return back(prev, nx)
        return prev

    def back(prev, sto):
        answer = []
        while sto != -1:
            answer.insert(0, sto)
            sto = prev[sto]
        return answer        
        
        
    def butforce(fpt, num, pak, ck=0):
        fpt = tuple(fpt)
        if m == 6:
            if ck:
                fpt = tuple([i if not 0 < i < 99 or i == pak else 50 for i in fpt])
            else:
                fpt = tuple([fpt[i] if not 0 < fpt[i] < 99 else 50 if 0<fpt[i]<50 or not chkd(i,num) else 60 for i in range(len(fpt))])
        if end(fpt,num,pak,ck):
            return []
        q, prev, answer = PriorityQueue(), {fpt: -1}, []
        q.put([hust(fpt, num, pak, ck), 0, fpt])
        while not q.empty():
            wait(0.000000000000000000000000001)
            w, pt = q.get()[1:]
            for x in [x for x in moving if 0 < pt[x] < 99]:
                ret = node(pt, x, None)
                for nx in ret:
                    if x == nx or pt[nx]:
                        continue
                    npt = exc(pt, x, nx)
                    if not npt in prev:
                        q.put([ hust(npt, num, pak, ck) + w, w + 1, npt])
                        prev[npt] = pt, ret, nx
                    if end(npt, num, pak, ck):
                        sto = pt, ret, nx
                        while sto != -1:
                            answer.insert(0,back(sto[1], sto[2]))
                            sto = prev[sto[0]]
                        return answer

    answer, answer_back,answer_end = [], [],[]
    if m == 6:
        vis = {1:[0,2,6,8],6:[0,12,1,13],29:[23,35,22,34],34:[33,35,27,29]}
        sto = {0:[],1:[]}
        fix = []
        for i in vis:
            if fpt[i] == 99:
                fix.extend(vis[i])
                sto[i//6//3].extend(vis[i][:2])
        for x in range(12):
            count = {0: [], 1: []}
            for k in moving:
                if 0 < fpt[k] < 50:
                    c = hust(fpt, k, fpt[k], 1) if not k in fix else 1000000
                    count[target.index(fpt[k])//6//3].append([c if not end(fpt, k, fpt[k], 1) else -1000, k])
            k = min(count[x % 2])[1]
            num = fpt[k]
            for i in butforce(fpt, k, fpt[k], 1):
                fpt = exc(fpt, i[0], i[-1])
                answer.append(i)
            fpt = list(fpt)
            fpt[fpt.index(num)] = 50
            if x%2:
                for nx in range(2):
                    if sto[nx%2]:
                        k = sto[nx%2].pop()
                        for i in butforce(fpt, k, 60):
                            fpt = exc(fpt, i[0], i[-1])
                            answer.append(i)
                        fpt = list(fpt)
                        fpt[k] = 99
                        for i in moving[k]:
                            if i in fix:
                                fix.remove(i)

    for k in pos:
        for i in butforce(target, [k], None):
            target = exc(target, i[0], i[-1])
            answer_back.append(i[::-1])
        for i in butforce(fpt, k, target[k]):
            fpt = exc(fpt, i[0], i[-1])
            answer.append(i)
        moving, bf = {i: [j for j in moving[i] if j != k] for i in moving if i != k}, {}

    if m == 5:
        for i in  butforce(target,[4,10],None):
            target = exc(target, i[0], i[-1])
            answer_back.append(i[::-1])

    if m != 6:
        answer.extend(butforce(fpt, None, None))

    for i in answer + answer_back[::-1]:
        sto, ret = [], []
        for x, nx in zip(i, i[1:]):
            T = (x in p and nx in p)
            ret.append([abs(x // m - nx // m), abs(x % m - nx % m)])
            if not sto or sto[-1][0] != T:
                if sto:
                    sto[-1][-1].extend([x])
                sto.append([T, [x]])
            else:
                if ret[-1] != ret[-2]:
                    sto[-1][-1].extend([x])
        sto[-1][-1].extend([nx]) # t append(nx)
        answer_end.extend(sto)

    return answer_end