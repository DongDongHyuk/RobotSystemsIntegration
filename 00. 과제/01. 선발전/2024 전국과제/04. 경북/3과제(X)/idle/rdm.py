import random
from printer import printf
def rdm(t):
    c = random.choice
    cs = random.sample
    if t == 0:
        pass
    if t == 1:
        m = list('x0000xxx00xx000000000000xx00xxx0000x')
        packs = list('123456789abc')
        for i in [1,2,3,4,8,9,26,27,31,32,33,34]:
            pack = c(packs)
            m[i] = pack
            packs.remove(pack)
        res = ''.join(m)
    if t == 2:
        pass
    return res
