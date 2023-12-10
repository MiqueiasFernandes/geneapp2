#!/bin/python3
import sys
from pathlib import Path

PROJECTS=sys.argv[1] ## /tmp/geneappdata/projects
PROJ=sys.argv[2]     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=sys.argv[3]       ## 99
INPUTS=f"{PROJECTS}/{PROJ}/inputs/"

## genome.fasta => anotattion.gff3 => transcriptome.fna => proteome.faa
GENOM=INPUTS+sys.argv[4]
ANOT=INPUTS+sys.argv[5]
TRANSCRIPT=INPUTS+sys.argv[6]
PROTEOM=INPUTS+sys.argv[7]

LOG=f"{PROJECTS}/{PROJ}/jobs/job.{ID}.out.txt"
ERR=f"{PROJECTS}/{PROJ}/jobs/job.{ID}.err.txt"
Path(LOG).touch()
Path(ERR).touch()

def log(msg):
    with open(LOG, 'a') as fo:
        fo.write(msg+'\n')

def err(msg):
    with open(ERR, 'a') as fo:
        fo.write(msg+'\n')

seqs = [x for x in open(GENOM) if x.startswith('>')]
log(f'{len(seqs)} found in fasta {GENOM}')
err(str(seqs))

print('TERMINADO_COM_SUCESSO')
