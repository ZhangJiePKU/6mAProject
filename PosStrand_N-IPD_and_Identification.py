from __future__ import division
import sys
import scipy.stats as stats
import numpy as np
from math import log

input_file=sys.argv[1]
col_num=int(sys.argv[3])
hole_name=sys.argv[2]
kz_file_nearA=sys.argv[4]
output_file_nearA=sys.argv[5]
output_file_variation=sys.argv[6]

file1=open(input_file,"r")
list1=file1.readlines()
file2=open(kz_file_nearA,"r")
list2=file2.readlines()

def test(group1,group2):
        u_statistic, pVal = stats.mannwhitneyu(group1, group2, alternative='greater')
        return pVal

def normalize(x,y):
        x_update=x.strip('\n').split()[1:]
        y_update=y.strip('\n').split()[1:]
        normalize_list_nearA=[]
        normalize_list_nearA.append(x.strip('\n').split()[0])
        for i,a in enumerate(x_update):
                if a == "*" or a == "-" or y_update[i] == "*" or y_update[i] == "-":
                        continue
                else:
                        if np.mean([int(a),int(y_update[i])]) == 0:
                                normalize_list_nearA.append(round(int(a)/1,2))
                        else:
                                normalize_list_nearA.append(round(int(a)/round(np.mean([int(a),int(y_update[i])]),3),3))

        return normalize_list_nearA

def str_float(x):
        x_update=[float(i) for i in x]
        return x_update

def fold_change_mean(x,y): #x: wt; y:kz
    if np.mean(str_float(y)) == 0:
        if np.mean(str_float(x)) == 0:
            fold_change="both_0"
        else:
            fold_change="inf"
    else:
        fold_change=log((np.mean(str_float(x))/np.mean(str_float(y))+1e-100),2)
    return fold_change

def fold_change_median(x,y):
    if np.median(str_float(y)) == 0:
        if np.median(str_float(x)) == 0:
            fold_change="both_0"
        else:
            fold_change="inf"
    else:
        fold_change=log((np.median(str_float(x))/np.median(str_float(y))+1e-100),2)
    return fold_change

def cv(x):
    if np.mean(str_float(x)) == 0:
        cv_value="NaN"
    else:
        cv_value=np.std(str_float(x))/np.mean(str_float(x))
    return cv_value

def count_margin(q1, q3):
        q4 = q3 + 1.5 * (q3 - q1)
        q5 = q1 - 1.5 * (q3 - q1)
        return q4, q5

def count_median_quartiles(lis):
        result=np.percentile(lis, [25, 50, 75])
        p25=result[0]
        p75=result[2]
        median=result[1]
        p25_margin=count_margin(p25,p75)[0]
        p75_margin=count_margin(p25,p75)[1]
        return [p25_margin,p25,median,p75,p75_margin]

def main():
# step 1: extract IPD values from the input file
        input_list=[]
        base=[]
        for i,a in enumerate(list1):
                b = []
                a=a.strip('\n').split()
                b=[j for j in a[(col_num*2+1):(col_num*3+1)]]
                base.append(a[col_num*2])
                if len(b) == 0:
                        input_list.append(str(a[0])+"\t"+"0"+"\n")
                else:
                        input_list.append(str(a[0])+"\t"+"\t".join(str(m) for m in b)+"\n")
# step 2: extract the coordinate --> pos:T neg:A
        T_pos=[l for l,m in enumerate(base) if m == "T"]

        nearA=[]
        for n,b in enumerate(T_pos):
                if n == 0:
#                       if b == 0:
                                nearA.append("-")
                else:
                        if T_pos[n]-T_pos[n-1] > 1:
                                nearA.append(T_pos[n]-1)
                        else:
                                for i in range(n):
                                        if T_pos[n-i]-T_pos[n-i-1] > 1:
                                                nearA.append(T_pos[n-i]-1)
                                                break
                                        else:
                                                if n-i-1 == 0:
#                                                       if T_pos[0] == 0:
                                                                nearA.append("-")
                                                else:
                                                        continue

# step 3: reduce variation --> output2
        output_nearA=[]
        output_nearA_list=[]
        for i,a in enumerate(T_pos):
                if nearA[i] == "-":
                        continue
                else:
                        nearA_ele=normalize(input_list[a],input_list[nearA[i]])
                        output_nearA.append("\t".join(str(m) for m in nearA_ele)+"\n")
                        output_nearA_list.append(nearA_ele)
# step 4: test --> output1
        result_nearA=[]

        if len(output_nearA_list)==0:
                result_nearA=[]
        else:
                kz_list_0=[i.strip('\n').split()[0] for i in list2]

                if max(len(i) for i in output_nearA_list) <= 5:
                        result_nearA=[]
                else:
                        for j,c in enumerate(output_nearA):
                                c=c.strip('\n').split()
                                if int(c[0]) != 0 and c[0] in kz_list_0:
                                        d=list2[kz_list_0.index(c[0])].strip('\n').split()
                                        if len(c[1:]) >= 5:
                                                result_nearA.append(hole_name+"\t"+str(c[0])+"\t"+str(fold_change_mean(str_float(c[1:]),str_float(d[1:])))+"\t"+str(fold_change_median(str_float(c[1:]),str_float(d[1:])))+"\t"+str(np.var(str_float(c[1:])))+"\t"+str(np.std(str_float(c[1:])))+"\t"+str(cv(str_float(c[1:])))+"\t"+str(np.var(str_float(d[1:])))+"\t"+str(np.std(str_float(d[1:])))+"\t"+str(cv(str_float(d[1:])))+"\t"+str(test(str_float(c[1:]),str_float(d[1:])))+"\t"+"\t".join(str(m) for m in count_median_quartiles(str_float(c[1:])))+"\t"+"\t".join(str(n) for n in count_median_quartiles(str_float(d[1:])))+"\n")
                                        else:
                                                continue
                                else:
                                        continue


        file4=open(output_file_nearA,'w')
        file4.writelines(result_nearA)
        file4.close()

        file5=open(output_file_variation,'w')
        file5.writelines(output_nearA)
        file5.close()

if __name__ == '__main__':
        main()
