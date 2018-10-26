---
title: 尝试提升ptyhon3运行效率
tags: python3,JIT,pypy3
grammar_cjkRuby: true
---
1. Biopython中`Bio.SubsMat.MatrixInfo.pam250`和`Bio.SeqIO`模块与`readfasta()`函数和`PAM250`字典的处理速度，两者无统计学上差异
	> 为了方便比较，统一使用`readsfasta()`和`PAM250`字典

2. python是解释型语言（区分于编译型语言）
	> python的执行过程
	> 源代码--python解释器(CPython/PyPy/Numba/Cython)-->字节码(pyc)--python解释器-->执行
	>   相对于默认菜单CPython，PyPy和Numba使用了JIT编译加速执行，Cython将Python代码编译成C源码，再把C源码转换成Python扩展模块
	> C的执行过程
	> 源代码--编译程序(gcc/clang/icc)-->目标代码--连接函数库-->二进制机器代码--执行

4. 初始代码
```python
from itertools import product
from Bio.SubsMat.MatrixInfo import pam250
from Bio import SeqIO
import numpy as np
import time


def swscore(s, t, penalty=-5):
    dp = np.zeros([len(s) + 1, len(t) + 1], dtype=np.int64)
    path = np.zeros([len(s), len(t)], dtype=np.int64)
    dp[0, :] = 0
    dp[:, 0] = 0
    for i, j in product(range(1, len(s) + 1), range(1, len(t) + 1)):
        cost = pam250.get((s[i - 1], t[j - 1]))
        if cost == None:
            cost = pam250.get((t[j - 1], s[i - 1]))
        # counterclockwise
        score = [
            dp[i - 1, j] + penalty,
            dp[i, j - 1] + penalty,
            dp[i - 1, j - 1] + cost,
            0
        ]
        index = score.index(max(score))
        path[i - 1, j - 1] = index
        dp[i, j] = score[index]

    return dp,path

def findpath(dp,path, i, j, seq1, seq2):
    seq1_edit = []
    seq2_edit = []
    while dp[i,j] != 0:
        # counterclockwise
        index = path[i - 1, j - 1]
        if index == 0:
            i, j = i - 1, j
            seq1_edit.append(seq1[i])
            seq2_edit.append('-')
        elif index == 1:
            i, j = i, j - 1
            seq1_edit.append('-')
            seq2_edit.append(seq2[j])
        elif index == 2:
            i, j = i - 1, j - 1
            seq1_edit.append(seq1[i])
            seq2_edit.append(seq2[j])
        elif index == 3:
            break
    return i, j, seq1_edit, seq2_edit


def main():
    start = time.time()
    file = 'input/rosalind_loca.txt'
    records = list(SeqIO.parse(file, "fasta"))
    seq1 = str(records[0].seq)
    seq2 = str(records[1].seq)
    dp,path = swscore(seq1, seq2)
    score = np.max(dp)
    print(time.time() - start)

if __name__ == "__main__":
    main()
```
> 使用PyCharm Profile分析
> ![enter description here](https://www.github.com/luyang93/gitimg/raw/master/2018/10/1540544498701.png)
5. 优化方案
