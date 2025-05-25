
def prt(m,y,x,z=1):
    di = {'x':' ','a':'①','b':'②','c':'③'}
    di = {'0':' ','1':'○','2':'△','3':'□','4':'●','5':'▲','6':'■'}
    di = {'x':' '}
    m = ''.join([di[i] if i in di else str(i) for i in m])
    for i in range(z-1,-1,-1):
        if z > 1:
            print(i+1,'Floor')
        print(''.join(['┌───',''.join(['┬───'] * (x - 1)),'┐']))
        for j in range(y):
            n = x * j
            print('│',' │ '.join(m[(0 + ((y * x) * i) + n):(x + ((y * x) * i) + n)]),'│')
            if j != y - 1:
                print(''.join(['├───',''.join(['┼───'] * (x - 1)),'┤']))
        print(''.join(['└───',''.join(['┴───'] * (x - 1)),'┘']))
    print()