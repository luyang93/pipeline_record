---
title: Survey_v1.4 流程说明
tags: survey,使用说明
grammar_cjkRuby: true
---

-----
# Overview
Survey_v1.4是在*de novo*组装中的一个模块，包括全基因组survey和初步组装两个功能。
Survey：通过kmer分析的方法，预测基因组大小，杂合率和重复序列概率。
初步组装：使用SoapDenovo进行初步组装，并对组装之后的Contig文件进行覆盖情况和GC含量的分析。
## v1.3 优化点：
1. 将kmer计数软件由soapKF 替换为jellyfish，缩短了运行时间;
2. 更改了输入方式，以配置文件的方式读入输入文件和参数；增加了一些运行参数；
3. 将流程中的绝对路径改为了相对路径，方便移植；
4. 添加了必要的注释和帮助信息，以及简单的运行日志；
## v1.4 优化点：
0. 使用snakemake对流程进行管理
1. 通过env.cfg配置流程，输入对应的参数，运行流程。
2. 根据需求，改变env.cfg中的['parameter']['run']参数，生成qc + survey + assembly, qc + survey, qc三种不同模块的报告。
3. 粒度化的控制资源请求，对于普通资源需求任务和高资源需求任务单独设置。
4. 不需要编辑.bashrc，不需要source环境变量文件，不会污染其他环境，用时生效，用过失效。

# Installation
```bash
git clone -b v1.0 git@bitbucket.org:RADnovogene/survey.git 00.survey/v1.0
git clone -b v1.2 git@bitbucket.org:RADnovogene/simple_report_modules.git 01.simple_report_modules/v1.2
```
# Requirements
- python(snakemake, lxml, BeautifulSoup4, requests, termcolor)
- R(ggplot2,cairo)
- perl(gzip)
```
conda create --name survey
source activate survey
conda install -c bioconda perl perl-io-gzip lxml beautifulsoup4 requests r r-ggplot2 cairo snakemake -y && conda install -c omnia termcolor -y
```
# Usage
```dsconfig
[general]
# sotfware
pipeline = /ifs/TJPROJ3/HWUS/USER/luyang/PIPELINE/00.survey/v1.0
R = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/bin
python = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/python3/bin
perl = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/python3/bin
snakemake = /ifs/TJPROJ3/RAD/luyang/SOFTWARE/miniconda3/envs/python3/bin
report_modules = /ifs/TJPROJ3/HWUS/USER/luyang/PIPELINE/01.simple_report_modules/v1.2/04.survey

[data]
name = nanjimaobei
file_list = /ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/03.test/nanjimaobei.list
qc_list = /ifs/TJPROJ3/HWUS/USER/luyang/DATA/nanjimaobei.QC/list.12.1

[parameter]
# run
## 0: none of survey, assemble or coverage_contig, only QC report
## 1: qc + survey
## 2: qc + survey + assemble + coverage_contig
run = 2
max_read_length = 150
survey_kmer = 17
assembly_kmer = 43

[sge]
default = -l vf=4g,p=1
# survey
jellyfish_count = -l vf=40g,p=20
# assemble
## grapeK63_pregraph step needs many memory, about genome size(g) * 100 ~ 200
grapeK63_pregraph = -l vf=200g,p=30 -P smp1024 -q tjsmp03_1024.q
grapeK63_contig = -l vf=50g,p=30
grapeK63_map = -l vf=50g,p=30
grapeK63_scaff = -l vf=50g,p=30
# coverage_contig doesn't need too much resource, use default

[report]
Quote_No= 2019Q2-PAG-01
Contract_No = Contract_NoXXXXXXXXX
Contract_Name = Plant and Animal Genome Survey
Title_Name = Plant and Animal Genome Survey Report
Project_principals = Novogene Corporation Inc.
Latin_Name = NameXXXXXXXXX
```
配置文件说明
- ['general']:指定了一些环境路径
	- pipeline是流程路径.
	- python是python3的路径.
	- perl是perl的路径.
	- snakemake是snakemake的路径.
	- report_modules是报告模块的路径.
- ['data']:主要为一些输入文件的路径,
	- name指定了在流程中运行时,使用的样品名称.
	- file_list指定了QC后的clean data文件
	- qc_list指定了QC步骤中的文库文件
``` 
file_list
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/data/nanjingmaobei/DES02651_L1_1_clean.rd.fq.gz
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/data/nanjingmaobei/DES02651_L1_2_clean.rd.fq.gz
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/data/nanjingmaobei/DES02651_L2_1_clean.rd.fq.gz
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/data/nanjingmaobei/DES02651_L2_2_clean.rd.fq.gz
```
```
qc_list
DES02651_L1	350
DES02651_L2	350
```


- parameter:指定了运行的参数
	- ['run']:控制了运行的三种需求,qc, qc + survey, qc + survey + assembly
	- ['max_read_length']:read 长度
	- ['survey_kmer']:survey kmer大小
	- ['assembly_kmer']组装kmer大小
- ['sge']:指定了提交任务的资源需求,列表中列出的为高资源任务,其余任务按照默认即可.按照 -l vf=200g,p=30 -P smp1024 -q tjsmp03_1024.q 填写,整体是一个字符串,不需要加-cwd, -V
- report:指定了报告中出现的一些内容:
	- Quote_No:引用编号
	- Contract_No:合同编号
	- Contract_Name:合同名称
	- Title_Name:鼠标悬停网页标签,展示的名称
	- Project_principals:出报告的部门
	- Latin_Name:'物种拉丁名'
# Run
1. 从流程路径下(/ifs/TJPROJ3/HWUS/USER/luyang/PIPELINE/00.survey/v1.0)拷贝Survey.sh,env.cfg到工作目录.
2. 在工作目录下编辑clean data路径文件.
3. 在工作目录下编辑env.cfg文件.
4. 在工作目录下bash Survey.sh
5. 在工作目录下nohup bash nohup_run.sh &,运行投递流程

# Tips
- 如果需要重新生成不同模块的报告,可以修改env.cfg中的run参数
- 移除05.Report和xxxx_upload目录,以及待上传的压缩文件
- 在工作目录下bash Survey.sh
- 在工作目录下nohup bash nohup_run.sh &,运行投递流程

# 流程结构
- run:0
	- survey
![survey0](https://www.github.com/luyang93/gitimg/raw/master/2019/5/survey0.png)
	- report
![report0](https://www.github.com/luyang93/gitimg/raw/master/2019/5/report0.png)

- run:1
	- survey
![survey1](https://www.github.com/luyang93/gitimg/raw/master/2019/5/survey1.png)
	- report
![report1](https://www.github.com/luyang93/gitimg/raw/master/2019/5/report1.png)

- run:2
	- survey
![survey2](https://www.github.com/luyang93/gitimg/raw/master/2019/5/survey2.png)
	- report
![report2](https://www.github.com/luyang93/gitimg/raw/master/2019/5/report2.png)
# 参考项目路径
```
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/05.release
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/04.snk
/ifs/TJPROJ3/HWUS/USER/luyang/PROJECT/01.survey/06.run0
```
# 背景链接
https://run-survey.readthedocs.io/en/latest/computing_resource.html  
https://note.youdao.com/ynoteshare1/index.html?id=3066a675de28d98df83ba91addd3e718&type=note