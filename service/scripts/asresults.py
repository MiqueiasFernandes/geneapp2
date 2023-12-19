#!/bin/python3
import sys
from pathlib import Path
from Bio import SeqIO
from datetime import datetime, timezone
import pandas as pd
import os

PROJECTS=sys.argv[1] ## /tmp/geneappdata/projects
PROJ=sys.argv[2]     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=sys.argv[3]       ## 99
INPUTS=f"{PROJECTS}/{PROJ}/inputs/"
RESULTS=f"{PROJECTS}/{PROJ}/results/"
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("S " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")

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

print(f"... ASRESULTS PY ...")


def main():
### lista/fasta de genes as
    das_rmats = []

    for file in os.listdir(RESULTS+"rmats"):
        if ".JCEC." in file:
            das_rmats.extend(pd.read_csv(RESULTS+"rmats/"+file, sep='\t')['GeneID'])

    das_rmats = set(das_rmats)
    das_t3dra = set()
    das_genes = list(das_rmats.union(das_t3dra))

    open(RESULTS+"das_genes.txt", "w").writelines([x+"\n" for x in das_genes])
    print("# DAS Genes ===>", len(das_genes))

    rna2gene = dict([x.strip().split(',') for x in open(RESULTS+"/transcript_gene_mapping.csv")][1:])
    das_rnas = [k for k, v in rna2gene.items() if v in das_genes]
    print("# DAS mRNAS ===>", len(das_rnas))
    open(RESULTS+"das_mrnas.txt", "w").writelines([x+"\n" for x in das_rnas])
    
    all_genes = SeqIO.parse(RESULTS+"genes.fa", "fasta")
    x = SeqIO.write([x for x in all_genes if x.id in das_genes], RESULTS+"das_genes.fa", "fasta")
    print("# DAS Genes persist ===>", x)

    all_rnas = SeqIO.parse(RESULTS+"transcripts.fa", "fasta")
    x= SeqIO.write([x for x in all_rnas if x.id in das_rnas], RESULTS+"das_mrnas.fa", "fasta")
    print("# DAS MRNAS persist ===>", x)
    
    all_ptnas = SeqIO.parse(RESULTS+"proteins.fa", "fasta")
    x = SeqIO.write([x for x in all_ptnas if x.id in das_rnas], RESULTS+"das_ptnas.fa", "fasta")
    print("# DAS PTNAS persist ===>", x)
    
    with open(RESULTS+"das_ptnas.inline.fa", "w") as fo:
        for seq in SeqIO.parse(RESULTS+"das_ptnas.fa", "fasta"):
            fo.write(f"{seq.id},{str(seq.seq)}\n")

    ls = 0
    with open(RESULTS+"genes.gff.min", "w") as gffo:
        with open(RESULTS+"genes.gff3") as gff:
            for line in gff:
                if line.startswith("#") or line.count("\t") != 8:
                    continue
                pts = line.strip().split("\t")
                if pts[2] == "gene":
                    if pts[-1][3:] in das_genes:
                        gffo.write(line)
                        ls += 1
                if pts[2] == "mRNA":
                    if pts[-1][3:].split(";")[0] in das_rnas:
                        gffo.write(line)
                        ls += 1
                if pts[2] == "exon" or pts[2] == "CDS":
                    if pts[-1][7:] in das_rnas:
                        gffo.write(line)
                        ls += 1
    print("GFF MIN lines ===>", ls)

status=f"{PROJECTS}/{PROJ}/results/status.txt"
open(status, "a")
if not "ASRESULTS ... ok!\n" in open(status).readlines():
    main()
else:
    print("skipping ASRESULTS last run")
main()
print('TERMINADO_COM_SUCESSO')
open(status, "a").write("ASRESULTS ... ok!\n")
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("E " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")
