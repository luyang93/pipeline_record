---
title: tigmint流程.md
tags: tigmint,使用说明
grammar_cjkRuby: true
---

1. 环境搭建
	- 安装依赖
	```
	conda install python=3.6 bedtools bwa samtools intervaltree pybedtools pysam abyss seqtk boost gcc quast links
	pip install statistics
	```
	conda中的statistics很久未更新，依赖python2.7
	- 获取tigmint
	``` sh
	wget https://github.com/bcgsc/tigmint/archive/1.1.2.zip
	unzip 1.1.2.zip
	mv tigmint-* tigmint
	```
	- 编译ARKS(依赖Boost C++ libraries，需要source activate tigmint)
	``` sh
	wget https://github.com/bcgsc/arks/archive/1.0.2.zip
	unzip 1.0.2.zip
	cd arks-*
	bash autogen.sh
	./configure --with-boost=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/lib --prefix=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARKS
	make install
	```
	- 编译ARCS(依赖Boost C++ libraries，需要source activate tigmint)
	``` sh
	wget https://github.com/bcgsc/arcs/archive/v1.0.5.zip
	unzip v1.0.5.zip
	cd arcs-*
	bash autogen.sh
	./configure --with-boost=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/lib --prefix=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARCS
	make install
	```
	- 直接conda安装tigmint
	``` sh
	conda install tigmint
	conda install abyss seqtk boost gcc quast links
	pip install statistics
	```
	近期刚上传conda，未测试相关依赖。
	~~bedtools bwa samtools intervaltree pybedtools pysam~~
2. 环境变量
	``` sh
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/tigmint/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARCS/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARKS/bin:$PATH
	export PATH=/ifs/TJPROJ3/Plant/wangruiru/software/longranger-2.1.2/longranger-cs/2.1.2/bin:$PATH
	export LD_LIBRARY_PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/lib:$LD_LIBRARY_PATH
	```
3. 流程使用
- 拷贝流程至项目文件,编辑环境变量文件,设置相关参数
```
cp /ifs/TJPROJ3/RAD/luyang/PIPELINE/tigmint -r path/to/project
vim path/to/project/env.cfg
bash path/to/project/prepare_script.sh
```
- 运行run_pipeline.sh提交任务
```
bash path/to/project/run_pipeline.sh
```
- 删除中间数据,节省存储空间
```
bash path/to/project/delete.sh
```
- 输出结果
```
path/to/project/tigmint/draft.tigmint.fa
```
4. 参数说明
```
[args]
# env
dependency = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/bin
tigmint = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/tigmint
basic = /ifs/TJPROJ3/Plant/wangruiru/software/longranger-2.1.2/longranger-cs/2.1.2/bin

# data
xgreads = /ifs/TJPROJ3/Plant/Plant_Assembly/NJ_cop-to_TJ/P101SC17090890-01_danshen_10X
fasta = /ifs/TJPROJ3/Plant/gaodan/P101SC17071042-01_danshen/11.10X_zuzhuang/curated.fasta_609M

# tigmint-molecule
# Maximum distance between reads in the same molecule [50000]
dist = 50000
# Minimum number of reads per molecule (duplicates are filtered out) [4]
reads = 4
# Minimum mapping quality [0]
mapq = 0
# Minimum ratio of alignment score (AS) over read length [0.65]
as-ratio = 0.65
# Maximum number of mismatches (NM) [5]
nm = 5
# Minimum molecule size [2000]
size = 2000

# tigmint-cut
# Number of parallel processes to launch [8]
processes = 8
# Window size used to check for spanning molecules (bp) [1000]
window = 1000
# Spanning molecules threshold (no misassembly in window if num. spanning molecules >= n [2])
spanning = 2
# Number of base pairs to trim at contig cuts (bp) [0]
trim = 0

# bwa mem
# Number of threads [8]
t = 8

# samtools sort
# Set number of sorting and compression threads [8]
threads = 8
```
- `env`
	- `dependency`:tigmint依赖(bedtoosl,bwa,samtools等)
	- `tigmint`:tigmint路径
	- `bacis`:longranger basic路径
- `data`
	- `xgreads`:10X genomics数据路径
	- `fasta`:draft.fasta路径
- `tigmint-molecule`
	- `dist`:Maximum distance between reads in the same molecule
	- `reads`:Minimum number of reads per molecule (duplicates are filtered out)
	- `mapq`:Minimum mapping quality
	- `as-ratio`:Minimum ratio of alignment score (AS) over read length
	- `nm`:Maximum number of mismatches (NM)
	- `size`:Minimum molecule size
- `tigmint-cut`
	- `processes`:Number of parallel processes to launch
	- `window`:Window size used to check for spanning molecules (bp)
	- `spanning`:Spanning molecules threshold (no misassembly in window if num. spanning molecules >= n [2])
	- `trim`:Number of base pairs to trim at contig cuts (bp) [0]
- `bwa mem`
	- `t`:Number of threads
- `samtools sort`
	- `threads`:Set number of sorting and compression threads