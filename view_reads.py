def reads_alignTocigar(read,read_idx):
        idx_None=[i for i, j in enumerate(read_idx) if j == None]
        read_list=list(read)
        for k in idx_None:
                read_list.insert(k,'-')
        return ["".join(read_list),idx_None]

def match(read,idx_tuples):
        idx_None=[i for i, j in enumerate(idx_tuples) if j[1] == None]
        read_list=list(read)
        read_update=[]
        for i in range(0, len(read_list), 1):
                if i not in idx_None:
                        read_update.append(read_list[i])
                else:
                        read_update.append('*')
        return [read_update,idx_None]

def view(idx_tuples,read):
        ref_idx=[]
        read_idx=[]
        for i in idx_tuples:
                ref_idx.append(i[1])
                read_idx.append(i[0]) 
#       ref_view=ref_alignTocigar(ref,ref_idx)
        read_addDel=reads_alignTocigar(read,read_idx) 
        read_view=match(read_addDel[0],idx_tuples) 
        #idx_None=read_only_match[1]+read_view[1]
        #idx_None.sort()
        idx1=[a for a, b in enumerate(read_view[0]) if b == "*"]
        idx2=[c for c, d in enumerate(ref_idx) if d == None]
        read_view_update = [read_view[0][e] for e in range(0, len(read_view[0]), 1) if e not in idx1]
        ref_idx_update = [ref_idx[f] for f in range(0, len(ref_idx), 1) if f not in idx2]
        return [read_view_update,ref_idx_update,read_view[1],read_addDel[1]]
