from DRCF import *


def hust(pt, target):
    count = 0
    for i in range(6):
        if pt[i + 6] == 0 and target[i + 6] in [pt[12], pt[13]]:
            count -= 100
        if pt[i + 6] == target[i + 6]:
            count -= 100
            if pt[i] == target[i] and pt[i]:
                count -= 2
    return count

def find_num(pt):
    ret1, ret2 = {}, {}
    for i in range(12):
        if not pt[i]:
            ret1[i % 6] = i
        if pt[i] and not i % 6 in ret2:
            ret2[i % 6] = i
    return list(ret1.values()), list(ret2.values())

def butforce(pta, target):
    pta, target = tuple(pta), tuple(target)
    q, prev, answer = PriorityQueue(), {pta[:12]: -1}, []
    q.put([hust(pta, target), 0, pta])
    while not q.empty():
        wait(0.000000000000000001)
        w, pt = q.get()[1:]
        for x in [12, 13]:
            for nx in find_num(pt)[not pt[x]]:
                npt = list(pt)
                npt[x], npt[nx] = npt[nx], npt[x]
                npt = tuple(npt)
                if not npt[:12] in prev:
                    q.put([hust(npt, target) + w, w + 0.5, npt])
                    prev[npt[:12]] = pt[:12], nx, x
                if npt == target:
                    sto = pt[:12], nx, x
                    while sto != -1:
                        answer.insert(0, sto[1:])
                        sto = prev[sto[0]]
                    return answer
                