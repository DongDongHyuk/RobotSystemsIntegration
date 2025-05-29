def heu1(m):
    ct1 = 0
    for i in range(9):
        di = {'00':0,'10':1,'11':1,'21':1,'20':2,'22':2,'12':3}
        pk = str(di[m[i]+m[i+9]])
        ct1 += pk == v1[i]
    for i in range(6):
        for j in range(3):
            n = [6,7,8,15,16,17][i]-(3*j)
            if m[n] != '0':
                break
        ct1 += m[n] == v2[i]
    for i in range(6):
        for j in range(3):
            n = [8,5,2,17,14,11][i]-j
            if m[n] != '0':
                break
        ct1 += m[n] == v3[i]
    return [ct1 == 21 and m.count('1') == 6 and m.count('2') == 6,-ct1]