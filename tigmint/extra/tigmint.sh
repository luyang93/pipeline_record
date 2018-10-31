#!/usr/bin/env bash
export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/bin:$PATH
export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/tigmint/bin:$PATH
export PATH=/ifs/TJPROJ3/Plant/wangruiru/software/longranger-2.1.2/longranger-cs/2.1.2/bin:$PATH

samtools faidx draft.fa
bwa index draft.fa
bwa mem -t8 -p -C draft.fa reads.fq.gz | samtools sort -@8 -tBX -o draft.reads.sortbx.bam
tigmint-molecule draft.reads.sortbx.bam | sort -k1,1 -k2,2n -k3,3n >draft.reads.molecule.bed
tigmint-cut -p8 -o draft.tigmint.fa draft.fa draft.reads.molecule.bed
