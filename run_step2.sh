# Step 1
cat plot_upAnddown.txt | while read line;do
        col_num=$(echo ${line} | awk '{print NF}')
        if [ ${col_num} -eq 5 ];then
                echo ${line} | awk '{print $0,$2/$4,$3/$5}' >> plot_upAnddown_result_tmp.txt
        fi
done

cat plot_upAnddown_result_tmp.txt | sort -k 7 -nr > plot_upAnddown_result.txt

# Step 2
cat total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt | awk '{print $1,$2,$4,$5}' | while read line2;do
        chrom=$(echo ${line2} | awk '{print $1}')
        strand=$(echo ${line2} | awk '{print $2}')
        position=$(echo ${line2} | awk '{print $3}')
        motif=$(echo ${line2} | awk '{print $4}' | sed 's/./&\ /g' | awk '{print $1,$2,"A",$4,$5}' | sed "s/ //g")

        echo "${chrom}_${strand}_${position} ${motif:0:3} 3" >> motif_detial.txt
        echo "${chrom}_${strand}_${position} ${motif:1:3} 2" >> motif_detial.txt
        echo "${chrom}_${strand}_${position} ${motif:2:3} 1" >> motif_detial.txt
done

cat motif_detial.txt | sed "s/ /\t/g" | sort -k 2 > motif_detial_sort.txt

rm -rf motif_detial.txt

# Step 3
total_num=$(cat total-Focus_6mA.0-based.seq.upstream100_control.up0-based.upseq.downstream100_control.down0-based.downseq.txt | wc -l)

cat plot_upAnddown_result.txt| awk '{print $1}' | while read line;do
        weidianshu=$(grep "${line}" motif_detial_sort.txt | awk '{print $1}' | sort | uniq | wc -l)
        echo ${weidianshu} $(echo "scale=6;${weidianshu}/${total_num}"|bc) >> sites_ratio.txt
done
cat plot_upAnddown_result.txt| awk '{print $1,$2,$3,$4,$5,$7}' | sed "s/ /\t/g" | sed '1i\motif\tcase_num\tcase_freq\tcontrol_num\tcontrol_freq\tfreq_odds' > 1.txt
cat sites_ratio.txt | sed "s/ /\t/g" | sed '1i\site_num\tsite_ratio'> 2.txt
paste 1.txt 2.txt | sed "s/ /\t/g" > inhouse.txt

rm -rf sites_ratio.txt 1.txt 2.txt

# Step 4
cat inhouse.txt | sed '1d' | awk '{print "range",$0}' | sed "s/ /\t/g" | sed '1i\category\tmotif\tcase_num\tcase_freq\tcontrol_num\tcontrol_freq\tfreq_odds\tsite_num\tsite_ratio' > ../bubble.txt # Your output file
