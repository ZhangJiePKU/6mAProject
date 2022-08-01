import pysam
import sys
import pandas as pd
import extractIPDandPW
import view_reads
import write_result

def main():
        bf = pysam.AlignmentFile(sys.argv[1],'rb')
        # subreads alignment info
        reads_query_alignment_sequence=[]
        reads_query_alignment_length=[]
        reads_query_alignment_start=[]
        reads_query_alignment_end=[]
        # raw subreads info
        reads_query_sequence=[]
        reads_query_length=[]
        reads_query_name=[]
        # related ref info
        reads_reference_end=[]
        reads_reference_id=[]
        reads_reference_length=[]
        reads_reference_start=[]
        reads_reference_name=[]
        reads_reference_sequence=[]

        reads_align=[]
        # extract ipd and pw
        reads_get_tag_ipd=[]
        reads_get_tag_pw=[]

        for r in bf:
                reads_query_alignment_sequence.append(r.query_alignment_sequence)
                reads_query_alignment_length.append(r.query_alignment_length)
                reads_query_alignment_start.append(r.query_alignment_start)
                reads_query_alignment_end.append(r.query_alignment_end)

                reads_query_sequence.append(r.query_sequence)
                reads_query_length.append(r.query_length)
                reads_query_name.append(r.query_name)

                reads_reference_end.append(r.reference_end)
                reads_reference_id.append(r.reference_id)
                reads_reference_length.append(r.reference_length)
                reads_reference_start.append(r.reference_start)
                reads_reference_name.append(r.reference_name)

                reads_align.append(r.get_aligned_pairs(matches_only=False, with_seq=False))
                reads_reference_sequence.append(r.get_reference_sequence)
                reads_get_tag_ipd.append(r.get_tag('ip'))
                reads_get_tag_pw.append(r.get_tag('pw'))

        view_list=[]
        ipd_pw_de=[]
        ipd_pw_list=[]

        mark=sys.argv[3]

        for i, j in enumerate(reads_query_sequence):
                view_list.append(view_reads.view(reads_align[i],j))
                ipd_pw_de.append(extractIPDandPW.decode(reads_get_tag_ipd[i].tolist(),reads_get_tag_pw[i].tolist(),mark))
                ipd_pw_list.append(extractIPDandPW.ipd_pw(view_list[i],ipd_pw_de[i][0],ipd_pw_de[i][1],reads_align[i]))

        # write result file
        output_path1=sys.argv[2]

        write_result.write_result(view_list,ipd_pw_list,reads_reference_start,reads_reference_end,output_path1,mark)

print("*** writen done ***")


if __name__ == '__main__':
        main()
