#!/bin/python3
import sys
from pathlib import Path
import re
from Bio import SeqIO
from datetime import datetime, timezone

PROJECTS=sys.argv[1] ## /tmp/geneappdata/projects
PROJ=sys.argv[2]     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=sys.argv[3]       ## 99
INPUTS=f"{PROJECTS}/{PROJ}/inputs/"
RESULTS=f"{PROJECTS}/{PROJ}/results/"
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("S " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")

GN=sys.argv[4]
GENOM=INPUTS+GN
AN=sys.argv[5]
ANOT=INPUTS+AN
GOUT=INPUTS+sys.argv[6]
AOUT=INPUTS+sys.argv[7]

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
    pass

status=f"{PROJECTS}/{PROJ}/results/status.txt"
open(status, "a")
if not "ASRESULTS ... ok!\n" in open(status).readlines():
    main()
else:
    print("skipping ASRESULTS last run")

print('TERMINADO_COM_SUCESSO')
open(status, "a").write("ASRESULTS ... ok!\n")
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("E " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")
