import random
from printer import printf
def rdm(t):
    c = random.choice
    cs = random.sample
    res = []
    if t == 0:
        m = list('0x0x00000000000000000x0x0')
        li = [0,4,5,9,10,14,15,19,20,24]
        for pack in '123456789a':
            pos = c([i for i in li if m[i] == '0'])
            m[pos] = pack
        res.append(''.join(m))
    if t == 1:
        m = ['0'] * 16
        m[c([9,10,13,14])] = 'x'
        for pack in '12345678':
            pos = c([i for i in range(16) if m[i] == '0'])
            m[pos] = pack
        res.append(''.join(m))
    if t == 2:
        pos = c([5,6,9,10])
        li = [pos,{5:6,6:5,9:10,10:9}[pos],pos]
        for i in range(3):
            m = ['0']*16
            m[li[i]] = 'x'
            for pack in '12345':
                pos = c([i for i in range(16) if m[i] == '0'])
                m[pos] = pack
            res.append(''.join(m))
    return res