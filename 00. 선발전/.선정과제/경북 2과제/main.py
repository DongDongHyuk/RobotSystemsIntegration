from queue import PriorityQueue
from collections import deque
set_accx(2500);set_velx(1500);set_accj(400);set_velj([150,150,180,225,225,225]);set_tool('tool')
drl_report_line(0)
begin_blend(25)
def PLC(address,val=[],y=1,x=1):
    ser = serial_open(port ='COM')
    plc = list('00RSB06%DW'+'%03d'%address)
    plc += [i for i in '{:02X}'.format(y*x)]
    if val != []:
        plc[2] = 'W'
        plc += '%04x'%(val&0xFFFF)
    ser.write([5]+[ord(i) for i in plc]+[4])
    wait(0.05 if val == [] else 0.02)
    if val == []:
        plc = ser.read(ser.inWaiting()).decode()
        val = [int(plc[10+i:14+i],16) for i in range(0,y*4*x,4)]
    serial_close(ser)
    return val[0] if type(val) != int and len(val) ==  1 else val
    
def go_z(z):
    movel([0,0,z,0,0,0],mod=1,a=800)

pak,T,prev = [0,0],0,-1
def griper_open(x):
    global pak,T,prev
    wait(0.05)
    set_tool_digital_outputs([-1,2]) if not T else (wait(0.15),PLC(40,0))
    wait(0.2)
    PLC(x,pak[T])
    pak[T] = 0
    
def griper_close(x):
    global pak,T,prev
    wait(0.05)
    set_tool_digital_outputs([1,-2]) if not T else PLC(40,1)
    wait(0.2)
    pak[T] = PLC(x)
    PLC(x,0)
    
def chg(pos,num):
    global pak,T,prev
    if T != num:
        if T: 
            amovej([0,0,0,0,0,-180 if pos[0][4] == 3 else 180],mod=1,a=1500)
        else:
            amovej([0,0,0,0,0,180 if pos[0][4] == 3 else -180],mod=1,a=1500)
        wait(0.6)
        T = not T

def prt(pt,y,x):
    for i in range(0,y*x,x):
        tp_log(str(pt[i:i+x]))
    tp_log(' ')
        
def up(pos,z=280):
    return trans(pos,[0,0,z-pos[2],0,0,0])    
    
def find_z(pos,x,m):
    z = Z[pak[T]]    
    z += Z[PLC(pos[x][2])]
    if m:
        z += Z[PLC(pos[(x+6)%12][2])]
    return z

def move(pos,x,n,m,z):
    global pak,T,prev
    if prev != x:
        movejx(up(pos[x][T],m),sol=pos[0][4])
        prev = x
    if z and not n and not T:
        set_tool_digital_outputs([-1,-1])
    movel(trans(pos[x][T],[0,0,find_z(pos,x,z),0,0,0]),r=1)
    griper_close(pos[x][2]) if n else griper_open(pos[x][2])
    if z or not n:        
        movel(up(pos[x][T],m))
    
def pt_mov(answer,pos,m):
    global pak,T,prev
    for k in answer:
        for i,j in enumerate(k[1]):
            if not i:
                num = PLC(pos[j][2])
                chg(pos,k[0] if pos != C else num in pos[0][3])
                move(pos,j,1,280,0)
                go_z(5)
            if k[1][-1] != j:
                movel(trans(pos[j][T],[0,0,Z[num]+5 ,0,0,0]),r=50,a=2500)
                set_tool_digital_outputs([-1,-1])
        movel(trans(pos[j][T],[0,0,Z[num]+5,0,0,0]),r=1,a=1700)            
        go_z(-5)    
        griper_open(pos[j][2])
        movel(up(pos[j][T]))
        prev = j
    prev = -1
    
def make(p,y,x):
    P = {}
    i = [(p[1][i] - p[0][i]) / (y-1) if y != 1 else 0 for i in range(6)]
    j = [(p[2][i] - p[0][i]) / (x-1) if x != 1 else 0 for i in range(6)]
    for k in range(y*x):
        P[k] = [(i[l] * (k//x)) + (j[l] * (k%x)) + p[0][l] for l in range(6)]
    return P

pta = PLC(100,[],1,12)+[0,0]
target_a = [12-i for i in range(6)]+[i+1 for i in range(6)]+[0,0]
ptb = PLC(200,[],3,3)
target_b = [13 + i for i in range(6)]+[0,0,0]
ptc = PLC(300,[],3,5)
ptc[5],ptc[9] = 99,99
target_c = [0,19,0,22,0,
                99,20,0,23,99,
                0,21,0,24,0]

for i in [2,7,12]:
    ptc[i],target_c[i] = PLC(300+i),PLC(300+i)

#ptd = [[0,0,0,99,99,99],[0,0,0,101,101,99],[0,0,0,99,101,99],[99,102,99,0,0,0],[99,102,102,0,0,0],[99,99,99,0,0,0]]
ptd = [0,0,0,99,99,99,
          0,0,0,101,101,99,
          0,0,0,99,101,99,
          99,102,99,0,0,0,
          99,102,102,0,0,0,
          99,99,99,0,0,0]
target_d = [25, 26, 27, 99, 99, 99,
            28, 29, 30, 101, 101, 99,
            0, 0, 0, 99, 101, 99,
            99, 102, 99, 0, 34, 31,
            99, 102, 102, 0, 35, 32,
            99, 99, 99, 0, 36, 33]
ptd1,ptd2 = PLC(400,[],3,3),PLC(410,[],3,3)       
target_d1,target_d2 = [0 for i in range(9)],[0 for i in range(9)]          

#pta = [3,10,4,12,5,11,2,7,1,9,6,8,0,0]
#target_a = [12,11,10,9,8,7,1,2,3,4,5,6,0,0]
#ptb =  [17,0,16,15,13,0,0,14,18]
#target_b = [13, 14, 15,16, 17, 18, 0, 0, 0]
#ptc = [0,23,101,24,0,99,19,103,22,99,0,20,102,21,0]
#target_c = [0,19,101,22,0,99,20,103,23,99,0,21,102,24,0]
#ptd = [0, 34, 25, 99, 99, 99,29, 35, 0, 101, 101, 99,33, 0, 26, 99, 101, 99,99, 102, 99, 0, 36, 28,99, 102, 102, 32, 27, 30,99, 99, 99, 0, 31, 0]
#target_d = [25, 26, 27, 99, 99, 99, 28, 29, 30, 101, 101, 99, 0, 0, 0, 99, 101, 99, 99, 102, 99, 0, 34, 31, 99, 102,102, 0, 35, 32, 99, 99, 99, 0, 36, 33]


a = [posx(444.12, 483.12, 180, 168.77, -89.98, -89.96),posx(406.43, 285.13, 180, 168.45, -90.02, -90.02),posx(444.12, 483.12, 180, 168.77, -89.98, -89.96)]
a_air = [posx(444.92, 481.77, 137, 169.44, -90, 90),posx(408.15, 284.22, 137, 169.4, -90.01, 89.96),posx(408.15, 284.22, 137, 169.4, -90.01, 89.96)]
b = [posx(229.71, 436.23, 180, 169.36, -90.01, -90.06),posx(244.27, 515.1, 180, 169.6, -90.01, -90.04),posx(151.06, 451.51, 180, 169.03, -89.99, -90.04)]
b_air = [posx(230.79, 434.7, 137, 169.43, -90, 89.95),posx(245.2, 513.71, 137, 169.37, -90.01, 89.96),posx(152.23, 449.72, 137, 169.42, -90, 89.98)]
d1 = [posx(104.81, 472.47, 180, 133.86, 90.01, 90.02),posx(49.18, 530.34, 180, 134.21, 90.02, 90.04),posx(47.61, 416.7, 180, 133.99, 90.02, 90.02)]
d1_air = [posx(103.93, 474.23, 136.74, 134, 90, -90),posx(48.21, 531.94, 137.2, 134.17, 90, -90),posx(46.88, 418.44, 136.37, 133.92, 90, -90)]
d2 = [posx(-44.73, 474.87, 180, 134.26, 90, 90),posx(-100.56, 532.37, 180, 134.68, 89.99, 89.99),posx(-101.73, 419.32, 180, 134.77, 90.04, 90.03)]
d2_air = [posx(-45.79, 476.29, 136.84, 133.86, 90, -90),posx(-101.46, 533.45, 137, 133.98, 90, -90),posx(-102.72, 420.33, 136.82, 134.13, 90.01, -89.99)]
c = [posx(-298.12, 353.92, 180, 164.45, 90.03, 90.02),posx(-276.53, 430.52, 180, 164.18, 90.01, 90.01),posx(-452.44, 397.37, 180, 164.48, 90.03, 90.01)]
c_air = [posx(-299.57, 355.01, 137.27, 164.62, 90, -90),posx(-278.07, 431.57, 137.19, 164.36, 90.01, -89.97),posx(-453.96, 398.03, 138.08, 164.72, 90.02, -89.99)]
a = make(a,6,1)
a_air = make(a_air,6,1)
b = make(b,3,3)
b_air = make(b_air,3,3)
c = make(c,3,5)
c_air = make(c_air,3,5)
d1 = make(d1,3,3)
d1_air = make(d1_air,3,3)
d2 = make(d2,3,3)
d2_air = make(d2_air,3,3)

A,B,C,D = {},{},{},{}
for i in range(12):
    A[i] = a[i%6],a_air[i%6],100+i,[1],3
    #PLC(A[i][2],pta[i])
for i in range(9):
    B[i] = b[i],b_air[i],200+i,[],3
    #PLC(B[i][2],ptb[i])
for i in range(15):
    C[i] = c[i],c_air[i],300+i,[22,23,24],2
    #PLC(C[i][2],ptc[i])

for i in range(9):
    x = (i//3) * 6 + (i%3)
    D[x] = d1[i],d1_air[i],400+i,[],2
    D[x+21] = d2[i],d2_air[i],410+i,[],2
    ptd[x]= ptd1[i]
    ptd[x+21]= ptd2[i]
    
    #target_d[i//3][i%3] = target_d[x]
    #target_d[i//3+3][i%3+3] = target_d[x+21]

    target_d1[i] = target_d[x]
    target_d2[i] = target_d[x+21]
    #PLC(D[x][2],ptd[x])
    #PLC(D[x+21][2],ptd[x+21])
    
#ptd,target_d = [ptd[i][j] for i in range(6) for j in range(6)],[target_d[i][j] for i in range(6) for j in range(6)]       
   
D[10] = [],posx(-27.1, 401.83, 136.48, 135.18, 90.53, -89.59)
D[25] = [],posx(-25.15, 550.18, 136.79, 135.13, 90.35, -89.76)
Z = [[1,2,13,19,25,26,7,8,16,22,31,32],[3,4,14,20,27,28,9,10,17,23,33,34],[5,6,15,21,29,30,11,12,18,24,35,36]]
Z = {j:40+(10*i) for i in range(3) for j in Z[i]}
Z[0] = 0

run_a = sub_program_run('pta').butforce
run = sub_program_run('ptb').run


#prt(pta,2,6)
#prt(target_a,2,6)
#
#prt(ptb,3,3)
#prt(target_b,3,3)
#
#prt(ptc,3,5)
#prt(target_c,3,5)
#
#prt(ptd,6,6)
#prt(target_d,6,6)
#
#prt(target_d1,3,3)
#prt(target_d2,3,3)
#
#
#exit()


PLC(30,1)
movej([90,0,90,90,-90,0])
answer_a = run_a(pta,target_a)
answer_b = run(ptb, target_b, [0], 3, {},[1,3,4,5,7])
answer_c = run(ptc, target_c,[0,14],5, {101:[19,22],102:[20,23],103:[21,24]},[]) 
answer_d = run(ptd, target_d, [],6,{101: [25 + i for i in range(6)], 102: [31 + i for i in range(6)]},[8,9,10,16,22,13,19,25,26,27])
for i,j in answer_a:
    chg(A,j%12)
    move(A,i,PLC(A[i][2]),400,1)
pt_mov(answer_b,B,3)
movej([90,0,90,90,45,0],)
T = 0 
pt_mov(answer_d,D,6)
ptd1 = PLC(400,[],3,3)
ptd2 = PLC(410,[],3,3)
D1,D2 = {},{}
for i in range(9):
    x = (i//3) * 6 + (i%3)
    D1[i] = D[x]
    D2[i] = D[x+21]
answer_d1 = run(ptd1, target_d1, [0], 3, {},[])
answer_d2 = run(ptd2, target_d2, [0], 3, {},[])
pt_mov(answer_d1,D1,3)
pt_mov(answer_d2,D2,3)

pt_mov(answer_c,C,5)
PLC(30,1)