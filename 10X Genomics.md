---
title: 10X Genomics
tags:supernovo, 使用说明
grammar_cjkRuby: true
---


10X Genomics 从头组装
流程使用
```
/PUBLIC/software/DENOVO/pipeline/03.assembly/surpernova/supernova-2.0.0/pipeline/supernova_2.0.0_Pipeline2 \
-fq <input fastq.gz> \
-cores 32 \
-mem 384 \
-g gemome_size(G) \
-o ./
```
生成pipeline.sh,提交pipeline.sh
例子
```
/PUBLIC/software/DENOVO/pipeline/03.assembly/surpernova/supernova-2.0.0/pipeline/supernova_2.0.0_Pipeline2	\
-fq /TJPROJ2/Denovo/Project/X101SC19011127-Z01_niao_10XG/01.qc/qc_0326_fiter_homo/BDHX190009207-2a-AK343*/03*/*gz \
-cores 30 \
-mem 500 \
-g 2.5 \
-o ./
```

评估组装结果
```
/PUBLIC/software/DENOVO/pipeline/03.assembly/Assembly_Evaluation/Assembly_Eval_sjm_v2.pl
```

使用sjm管理任务
```
/PUBLIC/software/DENOVO/pipeline/03.assembly/Assembly_Evaluation/Assembly_Eval_sjm_v2.pl \
--step 178 \
--intron_type mam \
--BUSCO_type aves_odb9 \
--species chicken pseudohap2.1.fasta
```


