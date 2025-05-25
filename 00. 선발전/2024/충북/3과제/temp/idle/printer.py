# from datetime import datetime

# n = datetime.now()
# print('')
# print('┌─────────────────────┐')
# print('│{} [{}]│'.format(n.date(),str(n.time())[:8]))
# print('└─────────────────────┘\n')

def prt(m,y,x,hole=[],z=1):
    di = {'x' : ' ',}
    m = ''.join([di[j] if j in di else 'H' if i in hole else str(j) for i,j in enumerate(m)])
    for i in range(z-1,-1,-1):
        if z > 1:
            print('{} Floor'.format(i+1))
        print(''.join(['┌───',''.join(['┬───'] * (x - 1)),'┐']))
        for j in range(y):
            n = x * j
            print('│',' │ '.join(m[(0 + ((y * x) * i) + n):(x + ((y * x) * i) + n)]),'│')
            if j != y - 1:
                print(''.join(['├───',''.join(['┼───'] * (x - 1)),'┤']))
        print(''.join(['└───',''.join(['┴───'] * (x - 1)),'┘']))
    print('')