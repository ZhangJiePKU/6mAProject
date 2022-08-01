# **6mA-Sniper: Quantifying 6mA Sites in Eukaryotes at Single-Nucleotide Resolution**

## Introduction

While N6-methyldeoxyadenine (6mA) modification has been linked to fundamental regulatory processes in prokaryotes, its prevalence and functional implications in eukaryotes are controversial. Here, we report 6mA-Sniper to quantify 6mA sites in eukaryotes at single-nucleotide resolution,  through adequate control for both cross-molecule and cross-subreads variations in single-molecule real-time sequencing. With 6mA-Sniper, we delineated an accurate 6mA profile in C. elegans with 2,034 sites, significantly enriched on sequences with the GGAG motif. Twenty-five of the 39 (or 64.1%) candidate 6mA events with MnlI restriction endonuclease sites were experimentally verified, demonstrating the feasibility of the method. The in-population conservation and the combinatorial emergence of adjacent sites indicate 6mA regulation as an epigenetic mark rather than a misincorporation via the nucleotide salvage pathway. Notably, these 6mA events are selectively constrained in general, suggesting their regulatory functions in the worms. In support of the functional relevance of this regulation, we report the dominant contribution of one methyltransferase, METL-9, in shaping the basal 6mA profile in C. elegans. Moreover, we detected a global increase in the 6mA levels in C. elegans strains  treated with P. aeruginosa infection, and identified 998 6mA sites that emerged specifically in the strains withafter the infection. These newly-emerged 6mA sites were enriched in stimulus response genes generally upregulated after infection, recapitulating the finding that a large portion of cross-strain genetic variants removing 6mA sites are associated with the decreased expression of the corresponding genes. We thus highlight 6mA regulation as a functional epigenetic regulatory process in the stress response in eukaryotes.

## Table of contents

- Content
- Contact

## Content

- **3-mer_motif.sh:** An inhouse script was developed to identify the enriched 3-mer sequences centered by 6mA sites, in contrast to random sequences as the negative control.

      Usage (Shell) : bash 3-mer_motif.sh <command 1> <command 2>
  
      Commands:
    
      command 1: Input file (.bed) (Chrom\tChromStart\tChromEnd\tComplementaryStrand)
    
      command 2: Output folder name
      
      (The scripts run_step1.sh and run_step2.sh will be called in 3-mer_motif.sh.)

- **6mA-Sniper pipeline:** Developed to identify 6mA events at single-nucleotide resolution.
  
  Step 1. Unique mapping
    
    The raw SMRT sequencing reads were mapped to the reference genome of the species of interest using pbmm2 (version 1.1.0). Please convert the file to Sam format.
  
  Step 2. Extract IPD and PW of each CCS reads of each chromosome
  
       Usage (python 3.6.2) : python <command 1> <command 2> <command 3> <command 4>
    
       Commands:
      
       command 1: 6mA-Sniper-Step2.py
       
       command 2: raw_IPD.txt (your result file)
       
       command 3: strand (info extracted from （Step 1) .sam files)
    
      (The scripts extractIPDandPW.py, view_reads.py and write_result.py will be called in 6mA-Sniper-Step2.py.)
     
   Step 3. Noise reduction and 6mA Identification
   
      

## Contact

- zhangjie_imm@pku.edu.cn
- pengqi@pku.edu.cn
