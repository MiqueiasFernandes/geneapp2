#!/bin/python3
import sys
from pathlib import Path
from Bio import SeqIO
from datetime import datetime, timezone

MIN_SEQ=1000000
MIN_G_SEQ=100

PROJECTS=sys.argv[1] ## /tmp/geneappdata/projects
PROJ=sys.argv[2]     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=sys.argv[3]       ## 99
INPUTS=f"{PROJECTS}/{PROJ}/inputs/"
RESULTS=f"{PROJECTS}/{PROJ}/results/"
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("S " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")
print(".... SPLITX ....")
GENOM=INPUTS+sys.argv[4]
ANOT=INPUTS+sys.argv[5]

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

def divide(fasta, gff, seqs, sufix):
    SeqIO.write([x for x in SeqIO.parse(fasta, "fasta") if x.id in seqs], fasta+sufix, "fasta")
    with open(gff)as fin:
        with open(gff+sufix, 'w') as fw:
            for line in fin:
                if line.split('\t')[0] in seqs:
                    fw.write(line)

seqs = sorted([(seq.id, len(seq)) for seq in SeqIO.parse(GENOM, "fasta")], key=lambda e: e[1])

if len(seqs) < 5:
    err(f"GENOM HAS FEW SEQS {seqs}!")
    exit(1)

mixed = [y[0] for x in zip(seqs, seqs[::-1]) for y in x][:len(seqs)]
pt_1 = mixed[0::5]
pt_2 = mixed[1::5]
pt_3 = mixed[2::5]
pt_4 = mixed[3::5]
pt_5 = mixed[4::5]

divide(GENOM, ANOT, pt_1, "_pt1")
divide(GENOM, ANOT, pt_2, "_pt2")
divide(GENOM, ANOT, pt_3, "_pt3")
divide(GENOM, ANOT, pt_4, "_pt4")
divide(GENOM, ANOT, pt_5, "_pt5")

print('TERMINADO_COM_SUCESSO')

open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("E " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")