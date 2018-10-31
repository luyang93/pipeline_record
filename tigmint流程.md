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
	~~bedtools bwa samtools intervaltree pybedtools pysam ~~
2. 环境变量
	``` sh
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/tigmint/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARCS/bin:$PATH
	export PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/ARKS/bin:$PATH
	export PATH=/ifs/TJPROJ3/Plant/wangruiru/software/longranger-2.1.2/longranger-cs/2.1.2/bin:$PATH
	export LD_LIBRARY_PATH=/ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/tigmint/lib:$LD_LIBRARY_PATH
	```
3. ARKS使用
	- 输入文件
		- Draft assembly fasta file
		- Interleaved linked reads file
			> Barcode sequence expected in the BX tag of the read header
			> run longranger basic on raw chromium reads to produce this interleaved file
		- CSV file listing barcode multiplicities