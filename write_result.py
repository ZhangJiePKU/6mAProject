import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def mismatch_process(merge_df,view_list):
        merge_df_update=merge_df.T.reset_index(drop=True).T
        df_list=merge_df.values.tolist()
        subreads_num=len(view_list)

        index_start_seq=subreads_num
        index_end_seq=index_start_seq+subreads_num-1

        index_ref=index_end_seq+1

        index_start_ipd=index_ref+1
        index_end_ipd=index_start_ipd+subreads_num-1

        index_start_pw=index_end_ipd+1
        index_end_pw=index_start_pw+subreads_num-1

        for idx1,line in enumerate(df_list):
                seq=line[index_start_seq:(index_end_seq+1)]
                for idx2,i in enumerate(seq):
                        if i != line[index_ref:(index_ref+1)][0] and i != "-":
                                #print(merge_df_update.loc[idx1][idx2+index_start_ipd])
                                merge_df_update.loc[idx1][idx2+index_start_ipd]="*"
                                #print(merge_df_update.loc[idx1][idx2+index_start_ipd])
                                merge_df_update.loc[idx1][idx2+index_start_pw]="*"
        return merge_df_update

def write_result(view_list,ipd_pw_list,reads_reference_start,reads_reference_end,output_path1,mark):
        # pos polishing
        # head+seq+tail
        min_pos=min(reads_reference_start)
        max_pos=max(reads_reference_end)
        result_seq=[]
        result_position=[]
        result_ipd=[]
        result_pw=[]
        #print(len(ipd_pw_list[0][0]))
        for i,p in enumerate(reads_reference_start):
                fill_num_start=p-min_pos
                fill_num_end=max_pos-reads_reference_end[i]
                result_seq.append([0]*fill_num_start+list(view_list[i][0])+[0]*fill_num_end)
                result_position.append([0]*fill_num_start+list(view_list[i][1])+[0]*fill_num_end)
                result_ipd.append([0]*fill_num_start+ipd_pw_list[i][0]+[0]*fill_num_end)
                result_pw.append([0]*fill_num_start+ipd_pw_list[i][1]+[0]*fill_num_end)
        #print(len([0]*fill_num_start),len(list(view_list[0][0])),len([0]*fill_num_end))
        #print(len([0]*fill_num_start),len(list(view_list[0][1])),len([0]*fill_num_end))
        #print(len([0]*fill_num_start),len(ipd_pw_list[0][0]),len([0]*fill_num_end))
        #print(len([0]*fill_num_start),len(ipd_pw_list[0][1]),len([0]*fill_num_end))
        #print(reads_reference_start)
        #print(reads_reference_end)

        # creat dataframe
        data_seq=pd.DataFrame(result_seq).T
        data_position=pd.DataFrame(result_position).T
        data_ipd=pd.DataFrame(result_ipd).T
        data_pw=pd.DataFrame(result_pw).T

        # stat of seq
        stat=[]
        stat_0=[]
        stat_A=[]
        stat_T=[]
        stat_G=[]
        stat_C=[]
        stat_=[]
        stat_0.append(list(np.array((data_seq==0).sum(axis=1).tolist())/round(len(reads_reference_start),2)))
        stat_A.append(list(np.array((data_seq=="A").sum(axis=1).tolist())/round(len(reads_reference_start),2)))
        stat_T.append(list(np.array((data_seq=="T").sum(axis=1).tolist())/round(len(reads_reference_start),2)))
        stat_G.append(list(np.array((data_seq=="G").sum(axis=1).tolist())/round(len(reads_reference_start),2)))
        stat_C.append(list(np.array((data_seq=="C").sum(axis=1).tolist())/round(len(reads_reference_start),2)))
        stat_.append(list(np.array((data_seq=="-").sum(axis=1).tolist())/round(len(reads_reference_start),2)))

        for j in range(len(stat_0[0])):
                if stat_0[0][j] > stat_A[0][j] and stat_0[0][j] > stat_T[0][j] and stat_0[0][j] > stat_G[0][j] and stat_0[0][j] > stat_C[0][j] and stat_0[0][j] > stat_[0][j]:
                        stat.append(0)
                elif stat_A[0][j] > stat_0[0][j] and stat_A[0][j] > stat_T[0][j] and stat_A[0][j] > stat_G[0][j] and stat_A[0][j] > stat_C[0][j] and stat_A[0][j] > stat_[0][j]:
                        stat.append("A")
                elif stat_T[0][j] > stat_0[0][j] and stat_T[0][j] > stat_A[0][j] and stat_T[0][j] > stat_G[0][j] and stat_T[0][j] > stat_C[0][j] and stat_T[0][j] > stat_[0][j]:
                        stat.append("T")
                elif stat_G[0][j] > stat_0[0][j] and stat_G[0][j] > stat_T[0][j] and stat_G[0][j] > stat_A[0][j] and stat_G[0][j] > stat_C[0][j] and stat_G[0][j] > stat_[0][j]:
                        stat.append("G")
                elif stat_C[0][j] > stat_0[0][j] and stat_C[0][j] > stat_T[0][j] and stat_C[0][j] > stat_G[0][j] and stat_C[0][j] > stat_A[0][j] and stat_C[0][j] > stat_[0][j]:
                        stat.append("C")
                elif stat_[0][j] > stat_0[0][j] and stat_[0][j] > stat_T[0][j] and stat_[0][j] > stat_G[0][j] and stat_[0][j] > stat_C[0][j] and stat_[0][j] > stat_A[0][j]:
                        stat.append("-")
                else:
                        stat.append("Warning") # equal...

        data_stat=pd.DataFrame(stat)
        #print(data_stat)
        # merge dataframe
        merge_df=pd.concat([data_position,data_seq,data_stat,data_ipd,data_pw],axis=1)

        # mismatch -> * and post_process
        merge_df_update_raw=mismatch_process(merge_df,view_list)

        #write
        merge_df_update_raw.to_csv(output_path1, sep='\t',index=False)
