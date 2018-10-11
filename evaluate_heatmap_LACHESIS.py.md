---
title: evaluate_heatmap_LACHESIS.py
tags: python3,使用说明
grammar_cjkRuby: true
---

1. 原理
	- 热点图中，该染色体与其他染色体的相关性进行2×2列联表的卡方检验，判断这两条染色体是否显著相关。
	-  4号染色体与5号染色体是否相关，如图所示。对该单元格的列联表进行卡方检验，获得p_value。
	- p_value
	- ![p_value](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-18-40.jpg "p_value")
	-  对整张表，按照真阳性，假阳性，假阴性，真阴性进行分类，计算[F_score](https://en.wikipedia.org/wiki/F1_score)。
	- F_socre
	- ![F_socre](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-18-46.jpg "F_socre")
2. 使用方法
	- 依赖：
		- numpy
		- scipy
		- xlsxwriter
	``` sh
	export PATH=/ALBNAS15/01.PROJECT/02.TEST/00.envs/python3/bin:$PATH
	```
	- 路径：
	> /ALBNAS15/01.PROJECT/02.TEST/99.luyang/SCRIPT/evaluate_heatmap_LACHESIS.py
	- 参数解释：
	``` sh
	python3 evaluate_heatmap_LACHESIS.py -m heatmap.txt路径 -b heatmap.chrom_breaks.txt路径 -t 显著性阈值(默认0.0001) 
	```
	- 示例
	``` sh
	python3 evaluate_heatmap_LACHESIS.py -m ./heatmap.txt -b ./heatmap.chrom_breaks.txt -t 0.0001
	```
3. 输出
	- 当前目录下输出，heatmap.xlsx
	- heatmap表，为染色体相关性的p值，p值越小，相关的可能性越大，红色为该阈值条件下显著性相关的染色体。
	- score表，为进行F_score分析的结果，右下角为F_score值。
4. 结果分析 
	- 对于同一个样本的不同参数的结果，F_score值越大，代表热点图的效果越好。 
	- 热点图与F_score的比较
	- 热点图
	- ![热点图](https://www.github.com/luyang93/gitimg/raw/master/2018/9/auto_output87.93.93_HiC_heatmap.jpg "热点图")
	- 显著性
	- ![显著性](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-26-24.jpg "显著性")
	- F_score
	- ![F_score](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-26-27.jpg "F_score")
	- 热点图
	- ![热点图](https://www.github.com/luyang93/gitimg/raw/master/2018/9/auto_output36.42.42_HiC_heatmap.jpg "热点图")
	- 显著性
	- ![显著性](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-26-31.jpg "显著性")
	- F_score
	- ![F_score](https://www.github.com/luyang93/gitimg/raw/master/2018/9/photo_2018-09-26_02-26-34.jpg "F_score")