---
title: fragsacff流程
tags: fragscaff, 使用说明
grammar_cjkRuby: true
---

 1. 算法说明
	 1. 选择有效的reads比对结果去做scaffolding：
		 1. fragScaff 只用 scaffolds的两端区域的links来做scaffolding，初步是边界10k(前10k和后10k), scaffolds中间的reads比对结果扔掉
		2. 提供一个N.bed 文件记录了scaffolds 的gap区域，R.bed纪录了scaffolds的repeat区域(相似度>97%)
		3. 根据 N.bed 和 R.bed文件，求得scaffolds前后两段含有 不超过 5k 非N非R的最远边界NBP < 10k，每个scaffolds有自己的NBP边界
		4. 根据 N.bed 和 R.bed文件，进一步扔掉有一半落在R或者N区域的比对结果
		5. 最后确定了每个scaffolds的NBP，和落在该边界以内的reads比对结果去做scaffolds的连接
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
		 - java,bowtie2,picard
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
4. 参数
	- fliter_length:过滤短的contig,5000(5M)
	- cut_size:每个cut的大小,100000000(100M)
	- 5M alignment 100M
	- mapping: MAPQ(q):20
	- alignment: q:97
	- fragscaff
		- E:
		- o:
		- c
		- t
		- r 