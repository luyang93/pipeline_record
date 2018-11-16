---
title: fragscaff_tigmint_ARKS组合评估.md
tags: ARKS,tigmint,fragscaff
grammar_cjkRuby: true
grammar_mermaid: true
---


# 软件版本

## fragscaff流程
```
/ifs/TJPROJ3/Plant/Pipeline/10XG/bin/10XGscaff_v2.1
```
## tigmint
[tigmint](https://github.com/bcgsc/tigmint)
```
tigmint --version
Tigmint 1.1.2
```
## ARKS
[ARKS](https://github.com/bcgsc/arks)
```
arks --version
VERSION: arks 1.0.2
```
## LINKS
[LINKS](https://github.com/bcgsc/links)
```
LINKS --version
LINKS [v1.8.6]
```
# 测试数据
## 基因组特征

## 10X数据
62G
```
/ifs/TJPROJ3/Plant/Plant_Assembly/NJ_cop-to_TJ/P101SC17090890-01_danshen_10X/*.fq.gz
```
# 组装方案
## fragscaff
```mermaid!
graph LR;
	dfaft.fa --> fragscaff
	10X --> fragscaff
	fragscaff --> fasta
```
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/10/1.png "1")
## tigmint+fragscaff
```mermaid!
graph LR;
	10X --> longranger[Long Ranger basic]
	longranger --> reads[Interleaved linked reads]
	draft.fa --> tigmint
	reads --> tigmint
	tigmint --> break.fa
	break.fa --> fragscaff
	10X --> fragscaff
	fragscaff --> fasta
```
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/10/2.png "2")
## tigmint+ARKS
```mermaid!
graph LR;
	10X --> longranger[Long Ranger basic]
	longranger --> reads[Interleaved linked reads]
	draft.fa --> tigmint
	reads --> tigmint
	tigmint --> break.fa
	reads --> ARKS
	break.fa --> ARKS
	ARKS --> fasta
```
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/10/3.png "3")
## ARKS
```mermaid!
graph LR;
	10X --> longranger[Long Ranger basic]
	longranger --> reads[Interleaved linked reads]
	reads --> ARKS
	draft.fa --> ARKS
	ARKS --> fasta
```
![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/10/4.png "4")
# 组装结果
fragscaff,tigmint,ARKS均使用默认参数进行测试
## fragscaff
Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                 412 |
Total  |         611,768,841 |         609,144,668
Max    |          10,668,331 |          10,614,412
n50    |           2,414,574 |           2,395,696
n90    |             758,348 |             758,348

----------------------------------------
## tigmint+fragscaff
Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                 418 |
Total  |         611,799,396 |         609,144,644
Max    |          10,668,328 |          10,614,412
n50    |           2,413,918 |           2,395,696
n90    |             758,567 |             758,348

----------------------------------------
## tigmint+ARKS
Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                 654 |
Total  |         609,164,468 |         609,144,668
Max    |           6,483,884 |           6,483,684
n50    |           1,455,412 |           1,455,312
n90    |             516,064 |             516,064

----------------------------------------
## ARKS
Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                646 |
Total  |        609,164,468 |        609,144,668
Max    |          6,483,884 |          6,483,684
n50    |          1,455,412 |          1,455,312
n90    |            516,064 |            516,064

----------------------------------------
# 评估分析
根据tigmint的算法,将10X的linked reads数据分组成molecules,molecules覆盖度少的区域是潜在的错误组装.
通过breakpoint的数量来评价无参基因组装的质量.
### 10X
| 组装方案  | breakpoint |
| - | - | 
| fragscaff | 10 |
| tigmint+fragscaff | 6 |
| tigmint+ARKS | 0 |
| ARKS | 8 |
| origin | 8 |
### Hi-C
| 组装方案  | input_breaks | breakpoints_iteration_2 | breakpoints_iteration_3 | breakpoints_iteration_4 | breakpoints_iteration_5 |
| - | - | - | - | - | - |
| fragscaff | 84 | 323 | 112 | 72 | 41 |
| tigmint+fragscaff | 88 | 325 | 106 | 52 | 41 |
| tigmint+ARKS | 65 | 455 | 125 | 85 | 105 |
| ARKS | 65 | 453 |169 | 83 | 78 |
| origin | 50 | 600 | 225 | 88 | 47 |
## 统计breakpoint
### 10X
![breakpoint](https://www.github.com/luyang93/gitimg/raw/master/2018/10/图片1.png "breakpoint")
``` shell
segment=$(awk '{print $4}' draft.tigmint.fa.bed | grep '-' | wc -l)
line=$(awk '{print $4}' draft.tigmint.fa.bed | grep '-' | grep -f - draft.tigmint.fa.bed | awk  '{print $1}' | uniq | wc -l)
expr $segment - $line
```
### Hi-C
根据输出的input_breaks和breakpoints_iteration_\*.txt来计算misassemblies
``` shell
wc input_breaks breakpoints_iteration_*.txt | awk '{print $2 - $1}'
```

## 调整repeat_area
### norepeats
Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |         450 |
Total  | 611,706,825 | 609,144,668
Max    |   7,031,421 |   6,957,049
n50    |   2,159,651 |   2,141,919
n90    |     697,263 |     694,652

----------------------------------------
### blast
269673793 repeat area(bp)

Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                  412 |
Total  |          611,792,719 |          609,144,668
Max    |           10,670,357 |           10,614,412
n50    |            2,414,574 |            2,395,696
n90    |              758,348 |              758,348

----------------------------------------
![blast](https://www.github.com/luyang93/gitimg/raw/master/2018/11/blast.png "blast")
### blast filter < 500
254128691 repeat area(bp)

Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                  399 |
Total  |          611,849,820 |          609,144,668
Max    |           10,844,098 |           10,792,017
n50    |            2,386,748 |            2,378,272
n90    |              808,838 |              803,772

----------------------------------------
![blast_filter](https://www.github.com/luyang93/gitimg/raw/master/2018/11/2018年11月16日09:54:04.png "blast_filter")
### blast fliter < 500 + start-end 10k merge
560988475 repeat area(bp)

Scaffolds | withGaps | withoutGaps
-: | -: | -:
Seqs   |                 829 |
Total  |         609,253,094 |         609,144,668
Max    |           4,134,085 |           4,134,085
n50    |           1,058,044 |           1,058,044
n90    |             393,839 |             393,839

----------------------------------------
![blast_fliter_expand](https://www.github.com/luyang93/gitimg/raw/master/2018/11/2018年11月16日09:57:33.png "blast_fliter_expand")