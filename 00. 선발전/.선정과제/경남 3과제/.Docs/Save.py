# def h2(m,li):
#     ct = 0
#     for pk in '1234567':
#         if pk in [m[i] for i in li]:
#             n1,n2 = li.index(m.index(pk)),li.index(leaf.index(pk))
#             st1 = [m[i] for i in li[n1:]+li[:n1] if m[i] != '0'][:2]
#             st2 = [leaf[i] for i in li[n2:]+li[:n2] if leaf[i] != '0'][:2]
#             if st1 == st2:
#                 ct -= 10000
#         else:
#             ct -= 100
#     return ct
# if n == 2 and h2(cur,li) == -70000::
#     break

    # if t == 0:
    #     global hli      # hole
    #     leaf = a[0]
    #     hli = a[1] if len(a)==2 else []      # hole
    #     li = [0,3,8,11]
    #     xli = [i for i in range(12) if m[i] == 'x']
    #     # isc = 0
    #     li = []
    #     if xli:
    #         x = xli[0]
    #         # isc = x in [5,6]
    #         li = [[4,8],[0,4,8],[3,7,11],[7,11],
    #                [0,8],[4,0,8,1,9,2,6,10][:3],[7,3,11,2,10,1,5,9][:3],[3,11],
    #                [4,0],[8,4,0],[11,7,3],[7,3]][x]
    #     seq = [i for i in li if i not in xli + hli]

    #     # if isc:         # temp
    #     #     li = [4,0,8] if x == 5 else [7,3,11]
    #     #     seq = [i for i in li if i not in xli + hli]
    #     #     isc = False

    #     # print(seq)
    #     # prt(m,3,4)
    #     # # prt(''.join(leaf1),3,4)
    #     # prt(''.join(leaf),3,4)
    #     # exit()

    #     hd,hdr = [],{}
    #     leaf1 = list(leaf[:])
    #     for i in seq:
    #         # if isc and [leaf1[i] != '0' for i in seq].count(1) == 7:
    #         #     break
    #         pk = leaf1[i]
    #         if pk == '0':
    #             r = src(-2,leaf1,i,hd)
    #             pk = leaf1[r[-1]]
    #             hd.append(i)
    #             hdr[i] = r
    #             leaf1[r[-1]],leaf1[i] = '0',pk
    #         # if not isc:
    #         m = src(1,m,''.join(leaf1),i,pk)
    #         fx[i] = 1
    #     # if isc:
    #     #     fxli(range(si),0)
    #     #     li = [2,6,10,9,8,4,0,1] if x==5 else [3,7,11,10,9,5,1,2]
    #     #     m = src(2,m,''.join(leaf1),li)
    #     # else:
    #     #     m = src(1,m,''.join(leaf1),-1,-1)
    #     m = src(1,m,''.join(leaf1),-1,-1)
    #     for i in hd[::-1]:
    #         res.append([hdr[i],int(m[i])])