sample=$1
type=$2
ref_path=/PATH/ce11.fa # Reference genome (Here, ce11 for C.elegans)
input_path=/PATH/${type}/tmp # Your output folder
output_path=/PATH/${type} # Your output folder

cat ${input_path}/${sample}*.txt | awk '{print $1,$2,$3}' | while read line;do
        chrom=$(echo ${line} | awk '{print $1}')
        strand=$(echo ${line} | awk '{print $2}')
        pos=$(echo ${line} | awk '{print $3+1}')

        bin=2 # 3mer

        control_site_left_tmp=$((${pos}*1-100))
        control_site_right_tmp=$((${pos}*1+100))

        if [ ${strand}x = "neg"x ];then
                control_site_left_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_left_tmp}-${control_site_left_tmp} | sed 1d)
                control_site_right_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_right_tmp}-${control_site_right_tmp} | sed 1d)
        else
                control_site_left_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_left_tmp}-${control_site_left_tmp} -i | sed 1d)
                control_site_right_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_right_tmp}-${control_site_right_tmp} -i | sed 1d)
        fi

        if [ ${control_site_left_base}x = "A"x ];then
                control_site_left=${control_site_left_tmp}
        else
                until [ ${control_site_left_base}x = "A"x ]
                do
                        control_site_left_tmp=$((${control_site_left_tmp}-1))
                        if [ ${strand}x = "neg"x ];then
                                control_site_left_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_left_tmp}-${control_site_left_tmp} | sed 1d)
                        else
                                control_site_left_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_left_tmp}-${control_site_left_tmp} -i | sed 1d)
                        fi
                done
                control_site_left=${control_site_left_tmp}
        fi

        if [ ${control_site_right_base}x = "A"x ];then
                control_site_right=${control_site_right_tmp}
        else
                until [ ${control_site_right_base}x = "A"x ]
                do
                        control_site_right_tmp=$((${control_site_right_tmp}+1))
                        if [ ${strand}x = "neg"x ];then
                                control_site_right_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_right_tmp}-${control_site_right_tmp} | sed 1d)
                        else
                                control_site_right_base=$(samtools faidx ${ref_path} ${chrom}:${control_site_right_tmp}-${control_site_right_tmp} -i | sed 1d)
                        fi
                done
                control_site_right=${control_site_right_tmp}
        fi

        range_end_left=$((${control_site_left}*1+${bin}))
        range_start_left=$((${control_site_left}*1-${bin}))

        range_end_right=$((${control_site_right}*1+${bin}))
        range_start_right=$((${control_site_right}*1-${bin}))

        range_end=$((${pos}*1+${bin}))
        range_start=$((${pos}*1-${bin}))

# samtools faidx: 1-based

        if [ ${strand}x = "neg"x ];then
                up_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start_left}-${range_end_left} | sed 1d)
        else
                up_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start_left}-${range_end_left} -i | sed 1d)
        fi

        if [ ${strand}x = "neg"x ];then
                down_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start_right}-${range_end_right} | sed 1d)
        else
                down_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start_right}-${range_end_right} -i | sed 1d)
        fi

        if [ ${strand}x = "neg"x ];then
                focus_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start}-${range_end} | sed 1d)
        else
                focus_seq=$(samtools faidx ${ref_path} ${chrom}:${range_start}-${range_end} -i | sed 1d)
        fi

        echo ${chrom} ${strand} "Focus_6mA" $((${pos}-1)) $(echo ${focus_seq} | tr [a-z] [A-Z]) "upstream100_control" $((${control_site_left}-1)) $(echo ${up_seq} | tr [a-z] [A-Z]) "downstream100_control" $((${control_site_right}-1)) $(echo ${down_seq} | tr [a-z] [A-Z]) >> ${output_path}/tmp/total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt
done

# focus
cat ${output_path}/tmp/total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt | awk '{print $5}' | sed 's/./&\ /g' | awk '{print $1,$2,"A",$4,$5}' | sed "s/ //g" | while read line2;do # note! 3mer
        echo ${line2:0:3} >> ${output_path}/tmp/focus_6mA_3mer.txt
        echo ${line2:1:3} >> ${output_path}/tmp/focus_6mA_3mer.txt
        echo ${line2:2:3} >> ${output_path}/tmp/focus_6mA_3mer.txt
done

count_focus=$(cat ${output_path}/tmp/focus_6mA_3mer.txt | wc -l)
cat ${output_path}/tmp/focus_6mA_3mer.txt | sort | uniq -c | sort -k 2 | while read line3;do

        freq_num=$(echo ${line3} | awk '{print $1}')
        motif=$(echo ${line3} | awk '{print $2}')
        freq=$(echo "scale=5;${freq_num}*1/${count_focus}*1" | bc)
        echo ${freq_num} ${freq} ${motif} >> ${output_path}/tmp/focus_6mA_3mer_plot_tmp.txt
done
# upstream
cat ${output_path}/tmp/total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt | awk '{print $8}' | sed 's/./&\ /g' | awk '{print $1,$2,"A",$4,$5}' | sed "s/ //g" | while read line4;do
        echo ${line4:0:3} >> ${output_path}/tmp/upstream_3mer.txt
        echo ${line4:1:3} >> ${output_path}/tmp/upstream_3mer.txt
        echo ${line4:2:3} >> ${output_path}/tmp/upstream_3mer.txt
done

count_upstream=$(cat ${output_path}/tmp/upstream_3mer.txt | wc -l)
cat ${output_path}/tmp/upstream_3mer.txt | sort | uniq -c | sort -k 2 | while read line5;do
        freq_num=$(echo ${line5} | awk '{print $1}')
        motif=$(echo ${line5} | awk '{print $2}')
        freq=$(echo "scale=5;${freq_num}*1/${count_upstream}*1" | bc)
        echo ${freq_num} ${freq} ${motif} >> ${output_path}/tmp/upstream_3mer_plot_tmp.txt
done
# downstream
cat ${output_path}/tmp/total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt | awk '{print $11}' | sed 's/./&\ /g' | awk '{print $1,$2,"A",$3,$4}' | sed "s/ //g" | while read line6;do
        echo ${line6:0:3} >> ${output_path}/tmp/downstream_3mer.txt
        echo ${line6:1:3} >> ${output_path}/tmp/downstream_3mer.txt
        echo ${line6:2:3} >> ${output_path}/tmp/downstream_3mer.txt
done

count_downstream=$(cat ${output_path}/tmp/downstream_3mer.txt | wc -l)
cat ${output_path}/tmp/downstream_3mer.txt | sort | uniq -c | sort -k 2 | while read line7;do
        freq_num=$(echo ${line7} | awk '{print $1}')
        motif=$(echo ${line7} | awk '{print $2}')
        freq=$(echo "scale=5;${freq_num}*1/${count_downstream}*1" | bc)
        echo ${freq_num} ${freq} ${motif} >> ${output_path}/tmp/downstream_3mer_plot_tmp.txt
done
# up and down
cat ${output_path}/tmp/upstream_3mer.txt ${output_path}/tmp/downstream_3mer.txt > ${output_path}/tmp/upAnddown_3mer.txt
count_upAnddown=$(cat ${output_path}/tmp/upAnddown_3mer.txt | wc -l)
cat ${output_path}/tmp/upAnddown_3mer.txt | sort | uniq -c | sort -k 2 | while read line8;do
        freq_num=$(echo ${line8} | awk '{print $1}')
        motif=$(echo ${line8} | awk '{print $2}')
        freq=$(echo "scale=5;${freq_num}*1/${count_upAnddown}*1" | bc)
        echo ${freq_num} ${freq} ${motif} >> ${output_path}/tmp/upAnddown_3mer_plot_tmp.txt
done

cat ${output_path}/tmp/focus_6mA_3mer_plot_tmp.txt | while read line9;do
        motif=$(echo ${line9} | awk '{print $3}')
        freq_num=$(echo ${line9} | awk '{print $1}')
        freq=$(echo ${line9} | awk '{print $2}')
        echo ${motif} ${freq_num} ${freq} $(awk '{if($3=="'"${motif}"'") print $1,$2}' ${output_path}/tmp/upstream_3mer_plot_tmp.txt) >> ${output_path}/tmp/plot_upstream.txt
        echo ${motif} ${freq_num} ${freq} $(awk '{if($3=="'"${motif}"'") print $1,$2}' ${output_path}/tmp/downstream_3mer_plot_tmp.txt) >> ${output_path}/tmp/plot_downstream.txt
        echo ${motif} ${freq_num} ${freq} $(awk '{if($3=="'"${motif}"'") print $1,$2}' ${output_path}/tmp/upAnddown_3mer_plot_tmp.txt) >> ${output_path}/tmp/plot_upAnddown.txt
done
