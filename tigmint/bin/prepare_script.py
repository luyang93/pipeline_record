#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : test.py
# @Date    : 18-10-29
# @Author  : luyang(luyang@novogene.com)
import os
import configparser


def index_genome(config):
    with open('index_genome.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
export PATH={dependency}:$PATH

cd {wdir}/tigmint
samtools faidx {wdir}/tigmint/draft.fa
bwa index {wdir}/tigmint/draft.fa
'''.format(**config['args']))


def link_file(config, source_files, target_files, parallel_index):
    with open('link_file.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
                    
[ -d {wdir}/tigmint ] || mkdir -p {wdir}/tigmint
[ -d {wdir}/data ] || mkdir -p {wdir}/data
[ -d {wdir}/basic ] || mkdir -p {wdir}/basic
[ -d {wdir}/alignment ] || mkdir -p {wdir}/alignment
[ -d {wdir}/log ] || mkdir -p {wdir}/log
[ -d {wdir}/err ] || mkdir -p {wdir}/err
            
cd {wdir}/data
ln -s {fasta} {wdir}/data/draft.fa
'''.format(**config['args']))
    for i in range(len(parallel_index)):
        with open('link_file.sh', 'a') as f:
            f.write('''
[ -d {wdir}/data/{2} ] || mkdir -p {wdir}/data/{2}
ln -s {xgreads}/{0} {wdir}/data/{2}/{1}
'''.format(source_files[2 * i], target_files[2 * i], parallel_index[i], **config['args']))
            f.write('''
ln -s {xgreads}/{0} {wdir}/data/{2}/{1}
'''.format(source_files[2 * i + 1], target_files[2 * i + 1], parallel_index[i], **config['args']))


def longranger_basic(config, parallel_index):
    for i in range(len(parallel_index)):
        tmp = 'basic_' + parallel_index[i] + '.sh'
        with open(tmp, 'w') as f:
            f.write('''
#!/usr/bin/env bash
export PATH={basic}:$PATH

cd {wdir}/basic
longranger basic --fastqs={wdir}/data/{0} --id=basic_{0} --sample=XG
'''.format(parallel_index[i], **config['args']))


def alignment(config, parallel_index):
    for i in range(len(parallel_index)):
        tmp = 'alignment_' + parallel_index[i] + '.sh'
        with open(tmp, 'w') as f:
            f.write('''
#!/usr/bin/env bash
export PATH={dependency}:$PATH

cd {wdir}/alignment
bwa mem -t {t} -p -C {wdir}/tigmint/draft.fa {wdir}/basic/basic_{0}/outs/barcoded.fastq.gz | samtools sort -@ {threads} -t BX -o {wdir}/alignment/draft.reads_{0}.sortbx.bam
'''.format(parallel_index[i], **config['args']))


def samtools_merge(config):
    with open('samtools_merge.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
export PATH={dependency}:$PATH

cd {wdir}/alignment
samtools merge -t BX {wdir}/alignment/draft.reads_*.sortbx.bam {wdir}/alignment/draft.reads.sortbx.bam
'''.format(**config['args']))


def tigmint_molecule(config):
    with open('tigmint_molecule.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
export PATH={dependency}:$PATH
export PATH={tigmint}:$PATH

cd {wdir}/tigmint
tigmint-molecule --dist {dist} --reads {reads} --mapq {mapq} --as-ratio {as-ratio} --nm {nm} --size {size} {wdir}/alignment/draft.reads.sortbx.bam | sort -k1,1 -k2,2n -k3,3n > {wdir}/tigmint/draft.reads.molecule.bed
'''.format(**config['args']))


def tigmint_cut(config):
    with open('tigmint_cut.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
export PATH={dependency}:$PATH
export PATH={tigmint}:$PATH

cd {wdir}/tigmint
tigmint-cut --processes {processes} --window {window} --spanning {spanning} --trim {trim} --fastaout {wdir}/tigmint/draft.tigmint.fa {wdir}/tigmint/draft.fa {wdir}/tigmint/draft.reads.molecule.bed
'''.format(**config['args']))


def run_pipeline(config, parallel_index):
    with open('run_pipeline.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash
date > {wdir}/date.txt
bash {wdir}/script/link_file.sh
qsub -cwd -l vf=4g,p=2 -j y -sync y -N index_genome -o {wdir}/log/index_genome.log -e {wdir}/err/index_genome.log {wdir}/script/index_genome.sh
{{
'''.format(**config['args']))
    with open('run_pipeline.sh', 'a') as f:
        threads = max(int(config['args']['t']), int(config['args']['threads']))
        for i in range(len(parallel_index)):
            f.write('''
{{
qsub -cwd -l vf=8g,p=1 -j y -sync y -N basic_{0} -o {wdir}/log/basic_{0}.log -e {wdir}/err/basic_{0}.log {wdir}/script/basic_{0}.sh
qsub -cwd -l vf=4g,p={1} -j y -sync y -N alignment_{0} -o {wdir}/log/alignment_{0}.log -e {wdir}/err/alignment_{0}.log {wdir}/script/alignment_{0}.sh
}} &
'''.format(parallel_index[i], threads, **config['args']))
        f.write('''
wait
qsub -cwd -l vf=4g,p=1 -j y -sync y -N samtools_merge -o {wdir}/log/samtools_merge.log -e {wdir}/err/samtools_merge.log {wdir}/script/samtools_merge.sh
}} &
qsub -cwd -l vf=4g,p=2 -j y -sync y -N tigmint_molecule -o {wdir}/log/tigmint_molecule.log -e {wdir}/err/tigmint_molecule.log {wdir}/script/tigmint_molecule.sh
qsub -cwd -l vf=8g,p=8 -j y -sync y -N tigmint_cut -o {wdir}/log/tigmint_cut.log -e {wdir}/err/tigmint_cut.log {wdir}/script/tigmint_cut.sh
date >> {wdir}/date.txt
''')

def delete_data(config):
    with open('delete.sh', 'w') as f:
        f.write('''
#!/usr/bin/env bash

rm -rf {wdir}/basic/basic_*/outs/barcoded.fastq.gz
rm -rf {wdir}/alignment/draft.reads_*.sortbx.bam
rm -rf {wdir}/alignment/draft.reads.sortbx.bam
'''.format(**config['args']))
def main():
    # 读取env.config
    cur_path = os.getcwd()
    config = configparser.ConfigParser()
    config.read(cur_path + '/env.cfg')

    # 设置工作目录
    config.sections()
    config.set('args', 'wdir', cur_path)

    # 获取10X数据
    files = os.listdir(config['args']['xgreads'])
    source_files = []
    target_files = []
    for file in files:
        if file.endswith('fq.gz'):
            source_files.append(file)
            tmp = file.replace('-', '_').split('_')
            tmp[0] = 'XG'
            tmp[2] = 'L' + tmp[2][1:].zfill(3)
            tmp[3] = 'R' + tmp[3]
            tmp[4] = '001.fastq.gz'
            target_files.append('_'.join(tmp))
    # 分块处理
    parallel_index = list(map(str, [i for i in range(0, int(len(target_files) / 2))]))

    # 创建script目录并切换
    if not os.path.exists(cur_path + '/script'):
        os.mkdir(cur_path + '/script')
    os.chdir(cur_path + '/script')

    # 链接10X数据和fasta
    link_file(config, source_files, target_files, parallel_index)

    # index_genome
    index_genome(config)

    # longranger_basic
    longranger_basic(config, parallel_index)

    # alignment
    alignment(config, parallel_index)

    # samtools_merge
    samtools_merge(config)

    # tigmint_molecule
    tigmint_molecule(config)

    # tigmint_cut
    tigmint_cut(config)

    # run_pipeline
    os.chdir(cur_path)
    run_pipeline(config, parallel_index)

    # delete
    delete_data(config)

if __name__ == "__main__":
    main()
