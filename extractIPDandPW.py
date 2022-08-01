## step 1. decode
def decode(ipd,pw,mark):
        idx_64_127_ipd=[i for i, j in enumerate(ipd) if j >=64 and j <= 127]
        idx_128_191_ipd=[i for i, j in enumerate(ipd) if j >=128 and j <= 191]
        idx_192_255_ipd=[i for i, j in enumerate(ipd) if j >=192 and j <= 255]

        idx_64_127_pw=[i for i, j in enumerate(pw) if j >=64 and j <= 127]
        idx_128_191_pw=[i for i, j in enumerate(pw) if j >=128 and j <= 191]
        idx_192_255_pw=[i for i, j in enumerate(pw) if j >=192 and j <= 255]

        for i in idx_64_127_ipd:
                ipd[i]=range(64, 192, 2)[range(64, 128, 1).index(ipd[i])]
        for i in idx_128_191_ipd:
                ipd[i]=range(192, 448, 4)[range(128, 192, 1).index(ipd[i])]
        for i in idx_192_255_ipd:
                ipd[i]=range(448, 960, 8)[range(192, 256, 1).index(ipd[i])]

        for i in idx_64_127_pw:
                pw[i]=range(64, 192, 2)[range(64, 128, 1).index(pw[i])]
        for i in idx_128_191_pw:
                pw[i]=range(192, 448, 4)[range(128, 192, 1).index(pw[i])]
        for i in idx_192_255_pw:
                pw[i]=range(448, 960, 8)[range(192, 256, 1).index(pw[i])]
        #print(len(ipd))

        if mark == "neg":
                ipd.reverse()
                pw.reverse()

        return [ipd,pw]

## step 2. align to reads
def ipd_pw(view_list,ipd_de,pw_de,idx_tuples):
        ipd_update=[]
        pw_update=[]
        for j in view_list[3]:
                ipd_de.insert(j,"-")
                pw_de.insert(j,"-")
        for i in range(0, len(ipd_de), 1):
                if i not in view_list[2]:
                        ipd_update.append(ipd_de[i])
                        pw_update.append(pw_de[i])
                else:
                        ipd_update.append("*")
                        pw_update.append("*")
        #ipd_de_del=ipd_pw_add_del(idx_tuples,ipd_update)
        #pw_de_del=ipd_pw_add_del(idx_tuples,pw_update)
        idx1=[a for a, b in enumerate(ipd_update) if b == "*"]
        idx2=[c for c, d in enumerate(pw_update) if d == "*"]
        ipd_update2 = [ipd_update[e] for e in range(0, len(ipd_update), 1) if e not in idx1]
        pw_update2 = [pw_update[f] for f in range(0, len(pw_update), 1) if f not in idx2]
        #print(len(ipd_de))
        return [ipd_update2,pw_update2]
        #return [ipd_de_del,pw_de_del]

def ipd_pw_add_del(idx_tuples,IpdRoPw):
        IpdRoPw_idx=[]
        for i in idx_tuples:
                IpdRoPw_idx.append(i[0])
        idx_del=[m for m, j in enumerate(IpdRoPw_idx) if j == None]
        for k in idx_del:
                IpdRoPw.insert(k,0)
        return IpdRoPw
