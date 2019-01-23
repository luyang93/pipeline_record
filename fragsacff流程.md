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
		1. contig的每一端点定义为一个nodeID。read比对到nodeID时，定义为hit。对于每一个nodeID，相同barcode的reads归为同一个groupID，对每一个groupID下的reads的hit计数。
		2. 对于每个nodeID下的groupID的hits数量进行过滤，小于c，就抛弃该nodeID下的groupID.
		3. 对每个nodeID下的groupID的数量进行频数分布统计，丢弃含有过少(d)或过多(D)数量groupID的nodeID
		4. 分别计算某一个nodeID与其他nodeID的之间共有的groupID的共享比例（交集/并集），对这些比例进行高斯分布统计（均值，标准差），计算该比例的概率密度，对该概率密度取-log10，获得score。保留共享比例大于均值，score>r的nodeID1-nodeID2。
		5. 统计每一对nodeID1-nodeID2的score，取一个整数score值为p，使得j/2比例的score大于该整数。再设定一个阈值，该阈值为1.5×M与u×p中较小者，为reicp。
		6. 对每一个nodeID，若其与超过a个其他nodeID有连接关系，则丢弃该node。否则，根据其score值从大到小排序，取前l个score，保留nodeID1-nodeID2。再根据nodeID1-nodeID2的score值之和过滤，如果其大于reicp，则保留，并将contig两端的nodeID的score值赋值1000
	3. 构建trunk
		1. 最小生成树,
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
		- 1C4G
	9. fragscaff_s1
		- fragscaff
		- 20C20G
	10. fragscaff_s3
		- fragscaff
		- 1C40G
3. 流程优化
	 1. reads mapping contig
		 - 使用bed对bam提前过滤，输出减小，mergebam压力减小
	 2. contig alignment contig
		 - contig切短比较(bowtie2)
		 - 提取contig的头尾比较
	3. 比对软件可选bowtie2/STAR，STAR整体速度更快
4. env.cfg文件
```dsconfig
[general]
# sotfware
fragscaff = /HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff
longranger = /HWNAS12/RAD/luyang/SOFTWARE/longranger
pigz = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
bowtie2 = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
blast = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
bedtools = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
samtools = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
star = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/fragScaff/bin
python = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/envs/python3/bin
perl = /HWNAS12/RAD/luyang/SOFTWARE/miniconda3/bin
# data
contig = /HWNAS12/RAD/luyang/PROJECT/00.fragScaff/data/danshen.fasta
reads = /HWNAS12/RAD/luyang/PROJECT/00.fragScaff/data/danshen
# parameters
# contig准备阶段过滤small contig,m = 3000
filter_length = 3000
cut_size = 100000000

[mapping]
# mapping阶段,samtools view -q 30
mapping_q = 30
mapping_F = 4
# software,bowtie2/STAR
software = STAR

[alignment]
alignment_q = 97

[fragscaff]
# 根据需求修改,建议E的值为1/2N75，不超过1/2N50,o为2E,E和o可以多个数字组合,数字数字之间用‘,’分割,不能有空格
fragscaff_p0 = -E 30000,20000 -o 60000,40000 -C 3,5,7 -j 1.5,1.25,1,0.75,0.5 -u 2,2.5,3 -p A
# fragscaff_p0 = -E 30000 -o 60000 -C 3,5,7 -j 1.5,1,0.5 -u 2,2.5,3 -p A
# 非必要不改动
fragscaff_p1 = -b 1 -G H
fragscaff_p2 = -r 1 -A -v -R
fragscaff_p3 = -v -V A -d 0.05 -D 0.95 -l 5 -a 20 -x 3000 -X 8000 -L 100 -M 200 -U 0 -g X -n N

[sge]
basic = -l vf=20g,p=8
# bowtie2 1C2G，STAR 8C20G
# index_mapping = -l vf=2g,p=1
index_mapping = -l vf=20g,p=8
# bowtie2 8C8G，STAR 8C20G
# mapping = -l vf=8g,p=8
mapping = -l vf=20g,p=8
mergebam = -l vf=2g,p=8
index_alignment = -l vf=1g,p=1
alignment = -l vf=4g,p=1
prepare_bed = -l vf=2g,p=1
fragscaff_r1 = -l vf=4g,p=1
fragscaff_r2 = -l vf=10g,p=10
fragscaff_r3 = -l vf=20g,p=1
```
5. 参数说明
- [general][filter_length]：小于此长度的contig都会被过滤。
- [general][cut_size]：blast切份比较，每份db的大小，默认每份db为100MB，每份query为5M。
- [general][contig]：contig.fasta文件的路径。
- [general][reads]：reads.fq.gz的文件夹路径，后缀名为fq.gz，文件夹下无其他不相关文件。
- [mapping][mapping_q]：比对结果SAM文件里的MAPQ，小于此值被过滤。
- [mapping][mapping_F]：比对结果SAM文件里的flag，4为未比对上。
- [alignment][alignment_q]：blast结果中的比对质量，小于此值被过滤。
- [fragscaff]：分两类参数，根据需求修改组(fragscaff_p0)和非必要不修改组(fragscaff_p1/2/3)，fragscaff_p0有2种默认参数，一种会输出90个结果，另一种会输出27种结果。
- [sge]：sge环境资源需求，-l vf=4g,p=10 -P=aliyun

6. 使用方法
	1. 拷贝相关文件，以华为云为例
		```	shell
		cp /HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff/fragscaff.sh ./
		cp /HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff/env.cfg ./
		```
	2. 修改env.cfg
	 - 指定软件路径
	 - 指定数据路径
	 - 设定相关参数
	3. 生成pipeline.sh脚本
		```shell
		bash fragscaff.sh
		```
	4. 提交任务
		- 使用-N job_name -hold_jid job_name控制任务依赖，会一次性提交所有任务，但只有当满足前置任务时，才会请求资源运行任务，不会造成额外占用资源。
		```shell
		bash pipeline.sh
		```
	5. 结果生成
		```shell
		/HWNAS12/RAD/luyang/PROJECT/00.fragScaff/fragscaff.STAR/07.result/result.fasta
		```
	6. 结果分析
		- /HWNAS12/RAD/luyang/PROJECT/00.fragScaff/fragscaff.STAR/result.xlsx
		- ![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2019/1/2019-01-23_13-39-27_创建的截图.png "2019-01-23 13-39-27 创建的截图")
		- score值为所有参考值中都处于中段的评价，所有参考值不会太高也不会太低。
	7. 拷贝转移相关结果
	8. 删除数据
		```shell
		bash delete.sh
		```
7. 测试路径
```shell
/HWNAS12/RAD/luyang/PROJECT/00.fragScaff/fragscaff.STAR
/HWNAS12/RAD/luyang/PROJECT/00.fragScaff/fragscaff.bowtie2
```
重要的事情说三遍，请从/HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff拷贝相关文件  
重要的事情说三遍，请从/HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff拷贝相关文件  
重要的事情说三遍，请从/HWNAS12/RAD/zhangjinbo/01.release/01.fragScaff拷贝相关文件

8. 迁移方法
	1. 依赖
		- fragScaff
		- longranger
		- pigz
		- blast
		- bedtools
		- samtools
		- STAR
		- bowtie2
		- parallel
		- python3(需包含pandas, numpy)
		- perl
	2. 环境
		- 方法1
		```shell
		conda create -n fragScaff -y
		source activate fragScaff
		conda install pigz blast bedtools samtools star bowtie2 parallel
		git clone https://github.com/RADnovogene/fragScaff.git
		```
		- 方法2
		```shell
		git clone https://github.com/RADnovogene/fragScaff.git
		conda env create -f fragScaff.yaml
		```
	3. 修改env.cfg和fragscaff.sh
		- fragscaff.sh中的绝对路径需要修改
		- env.cfg中的依赖的PATH需要修改