---
tags: canu,issue
grammar_cjkRuby: true
---
- utgovl slow  
[utgovl step extremely slow](https://github.com/marbl/canu/issues/947)  
[long running time on unitig/1-overlap](https://github.com/marbl/canu/issues/994)
- obtovl slow  
[Long obtovl jobs. Switch to mhap?](https://github.com/marbl/canu/issues/1014)  
[overlap.sh running for 22 hours. Long reads, very small genome.](https://github.com/marbl/canu/issues/414)  
[obtovl takes days to deal with R9.4 nanopore data](https://github.com/marbl/canu/issues/437)  
[Canu takes over a week for one assembly](https://github.com/marbl/canu/issues/311)
- cor slow  
[Canu at 'cormhap' step for > 10 days for a 25M genome](https://github.com/marbl/canu/issues/942)
- solution  
```shell
overlapper=mhap
obtReAlign=true
utgReAlign=true 
```
or
```shell
obtOvlErrorRate=0.025
ovlMerThreshold=500
```
~~obtErrorRate=0.025  
utgOvlErrorRate=0.025  
utgErrorRate=0.025~~  
[Assembly of a human genome from nanopore sequencing data](https://genomeinformatics.github.io/NA12878-nanopore-assembly/)

