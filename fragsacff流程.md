---
title: fragsacff流程
tags: fragscaff, 使用说明
grammar_cjkRuby: true
---

 1. 算法说明
	 1. 选择有效的reads比对结果去做scaffolding：
		 1. fragScaff 只用contig的两端区域的links来做scaffolding，初步是边界10k(前10k和后10k), contig中间的reads比对结果扔掉
		2. 提供一个N.bed 文件记录了contig 的gap区域，R.bed纪录了contig的repeat区域(相似度>97%)
		3. 根据 N.bed 和 R.bed文件，求得contig前后两段含有 不超过 5k 非N非R的最远边界nBP < 10k，每个contig有自己的nBP边界
		4. 根据 N.bed 和 R.bed文件，进一步扔掉有一半落在R或者N区域的比对结果
		5. 最后确定了每个contig的NBP，和落在该边界以内的reads比对结果去做contig的连接
	2. 结构nodeID-groupID-hits
		0. contig的每一端点定义为一个nodeID。read比对到nodeID时，定义为hit。对于每一个nodeID，相同barcode的reads归为同一个groupID，对每一个groupID下的reads的hit计数。
		1. 对于每个nodeID下的groupID的hits数量进行过滤，小于c，就抛弃该nodeID下的groupID.
		2. 对每个nodeID下的groupID的数量进行频数分布统计，丢弃含有过少(d)或过多(D)数量groupID的nodeID
		3. 分别计算某一个nodeID与其他nodeID的之间共有的groupID的共享比例（交集/并集），对这些比例进行高斯分布统计（均值，标准差），计算该比例的概率密度，对该概率密度取-log10，获得score。保留共享比例大于均值，score>r的nodeID1-nodeID2。
		4. 统计每一对nodeID1-nodeID2的score，取一个整数score值为p，使得j/2比例的score大于该整数。再设定一个阈值，该阈值为1.5×M与u×p中较小者，为reicp。
		5. 对每一个nodeID，若其与超过a个其他nodeID有连接关系，则丢弃该node。否则，根据其score值从大到小排序，取前l个score，保留nodeID1-nodeID2。再根据nodeID1-nodeID2的score值之和过滤，如果其大于reicp，则保留，并将contig两端的nodeID的score值赋值1000
 2. 流程模块:
	 ![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/11/2.png "2")
	 1. index_mapping
		 - bowtie2,samtools
		 - 2C2G
	2. index_alignment
		- blast
		- 1C1G
	3. longranger_basic
		- longranger,pigz
		- 8C8G
		- 1G fq.gz对应8G内存,3h;6G fq.gz对应24G内存,20h;pigz默认4×2CPU
	4. alignment
		- blast
		- 1C4G
		- 5M vs 100M,最大内存35G,最长时间16h,内存资源需求不稳定
		- CPU推荐1C,2C×4不如1C×8
	5. mapping
		- bowtie2,samtools
		- 8C8G
	6. preparebed
		- bedtools
		- 1C2G
	7. mergebam
		- samtools
		- 1C2G
	8. fragscaff_s1
		- fragscaff
		- CG
	9. fragscaff_s1
		- fragscaff
		- CG
	10. fragscaff_s3
		- fragscaff
		- CG
 3. 流程优化
	 1. reads mapping contig
		 - 使用bed对bam提前过滤，输出减小，mergebam压力减小
	 2. contig alignment contig
		 - contig切短比较(bowtie2)
		 - 提取contig的头尾比较
4. env.cfg文件
```dsconfig
[general]
# sotfware
longranger = /ALNAS01/software/PUBLIC/longranger-2.1.6/longranger-cs/2.1.6/bin
pigz = /ALNAS01/software/PUBLIC/pigz-2.3.4
fragscaff = /ALBNAS15/01.PROJECT/02.TEST/99.luyang/PIPELINE/fragScaff
bowtie2 = /ALNAS01/software/PUBLIC/bowtie2-2.2.2
blast = /ALNAS01/software/PUBLIC/ncbi-blast-2.2.28+/bin/
bedtools = /ALBNAS15/01.PROJECT/02.TEST/00.software/anaconda2/bin
samtools = /ALBNAS15/01.PROJECT/02.TEST/00.software/anaconda2/bin
# data
contig = /ALBNAS12/Plant/Project/WORK/ALNAS13/HLM_SSPACE-LongRead/quiver/quiver_after_pb1213_0202/tasks/pbcoretools.tasks.gather_contigset-1/file.contigset.fasta
reads = /ALBNAS12/Plant/Project/WORK/ALNAS13/HLM_SSPACE-LongRead/10X_data
# parameters
fliter_length = 5000
cut_size = 100000000

[longranger]
sge_basic = -l vf=8g,p=8 -P aliyun

[mapping]
q = 20
F = 4
sge_index_mapping = -l vf=2g,p=2 -P aliyun
sge_mapping = -l vf=8g,p=8 -P aliyun
sge_mergebam = -l vf=2g,p=1 -P aliyun

[alignment]
q = 97
sge_index_alignment = -l vf=1g,p=1 -P aliyun
sge_alignment = -l vf=4g,p=1 -P aliyun
sge_prepare_bed = -l vf=2g,p=1 -P aliyun

[fragscaff]
# contig准备阶段已经过滤small contig
# fliter_length = 5000
# m = 5000
# mapping阶段,samtools view -q 20
# q = 20
fragscaff_s1 = -E 30000 -o 60000
# 一般不改动
# -d 0.05 -D 0.95 -l 5 -a 20 -U 0 -p A -v yes
# 根据需求修改
# -C 5 -t 20 -r 1 -M 200
fragscaff_s2 = -d 0.05 -D 0.95 -l 5 -a 20 -U 0 -p A -v yes -C 5 -t 20 -r 1 -M 200
# 一般不改动
# -L 100 -x 3000 -X 8000 -V A -p A
# 根据需求修改,j和u可以多个数字组合,数字数字之间用‘,’分割,不能有空格
# -j 1.25,2,3 -u 2,4,1
fragscaff_s3 = -L 100 -x 3000 -X 8000 -V A -p A -j 1.25,2,3 -u 2,4,1
sge_fragscaff_s1 = -l vf=4g,p=1 -P aliyun
sge_fragscaff_s2 = -l vf=20g,p=20 -P aliyun
sge_fragscaff_s3 = -l vf=8g,p=1 -P aliyun
```
5. 参数说明
	1. fragscaff_s1

-b 1	python预设，make bamParse then exit
-B barcoded.bam	python预设
-J Repeats.bed	python预设
-N Nbase.bed	python预设
-G H	H = after hash (name#group),bam的QNAME格式，python预设
-m 1	最小contig长度，先前已经处理，如果需要，加上也可以
-q 10	alignment最小质量值，先前已经处理，已经注释，参数无效
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/12/1543993304203.png)

	2. fragscaff_s2

-d 0.05	根据node上groupID的数量，过滤前5%
-D 0.95	根据node上groupID的数量，过滤前95%
-l 5	node上link的数量的下限，取前l个link，不足就取完
-a 20	node上link的数量的上限，超过丢掉node上所有link
-U 0	每个node最小的groupID数量
-p A	A自动确定，最终确定使用的，link最小质量值
-v yes	保留临时文件
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/12/1543993344726.png)

-C 5	过滤read_hit_node<C的groupID，需保留
-t 20	thread数量，不使用Q，因为天津不允许计算节点qsub
-r 1	link最小质量值，r越大，保留的link越多
-M 200	link最大质量值，大于M，都调低至M
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/12/1543993352404.png)

	3. fragscaff_s3

-V A	输出所有的graph files
-p A	A自动确定，最终确定使用的，link最小质量值
-L 100	fasta，每一行碱基数量
-x 3000	scaffold中最小N的数量，link的score高
-X 8000	scaffold中最大N的数量，link的score低

![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/12/1543993384063.png)

-C 5	过滤read_hit_node<C的groupID，需保留
-j 1.25	mean links per p-bin，过滤小于
-u 2	相互link的score阈值的倍数，u×j
![enter description here](https://markdown.xiaoshujiang.com/img/spinner.gif "[[[1543993389916]]]" )