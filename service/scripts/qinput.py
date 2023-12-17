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

seqs = [x for x in open(GENOM) if x.startswith('>')]
log(f'#{len(seqs)} found in fasta {GENOM}')

print(f"... QINPUT PY ...")

FILE_GENOME=GENOM
FILE_GFF=ANOT
GENOM_OUT=GOUT
GFF_OUT=AOUT
MIN_FRG=100
MAX_FRG=1000000
MIN_CHR=1000000
MAX_CHR=1000000000
MAX_CHRS=100
MIN_SEQS=1
MAX_SEQS=1000000
GEN_RGX = re.compile(r"^[actgnrykmswbdhvACTGNRYKMSWBDHV]+$")
PTN_RGX = re.compile(r"^[a-zA-Z]+$")

def clean_fasta(fin, fout, rgx, min_len, max_len, nseqs, stats=None):
    bp_seqs = lambda : SeqIO.parse(fin, "fasta")
    seqs = sorted([[x.id, len(x), 
                    not rgx.match(str(x.seq)) is None, 
                    len(x) < max_len, len(x) > min_len, False] 
                    for x in bp_seqs()], key=lambda e: -e[1])

    seqs_val, seqs_inv = [], []
    for seq in seqs:
        if len(seqs_val) < nseqs:
            seq[5] = True
            if seq[2] and seq[3] and seq[4]:
                seqs_val.append(seq[0])
                continue
        seqs_inv.append(seq[0])
    assert len(seqs_val) >= MIN_SEQS
    SeqIO.write([x for x in bp_seqs() if x.id in seqs_val], fout, "fasta")
    tt, sv, si =  len(seqs), len(seqs_val), len(seqs_inv)
    print("Valid seqs:", sv, f"{int(sv / tt *100)}%")
    print("Invalid seqs:", si, f"{int( si / tt *100)}%")
    print("Total seqs:", tt)
    v, i = ([x for x in seqs if x[0] in z] for z in [seqs_val, seqs_inv])
    if stats:
        open(stats, "w").writelines(["\t".join(map(str, x))+"\n" for x in i])
    return v, i

def get_parts(gff, tp):
    for l in open(gff):
        if l.startswith("#"): continue
        fs = l[:200].strip().split("\t")
        if len(fs) != 9 or fs[2] != tp: continue
        seq, _, tp, start, end, _, strand, frame, anots,  = fs
        id =  anots.split("ID=")[1].split(";")[0] if "ID=" in anots else None
        parent = anots.split("Parent=")[1].split(";")[0] if "Parent=" in anots else None
        yield l, seq, tp, int(start), int(end), strand, frame, id, parent

def clean_gff(gffin, seqs=None):
    for t in ["gene", "mRNA", "exon", "CDS"]:
        for L, seq, _, start, end, strand, frame, id, parent in get_parts(gffin, t):
            try:
                assert len(seq) > 0
                assert start <= end and start > 0
                assert strand == "+" or strand == "-"
                assert float("0"+frame) < 3
                assert t == "exon" or t == "CDS" or len(id) > 1
                if (not seqs is None) and (not seq in seqs): continue
                yield seq, None, t, start, end, None, strand, frame, id, parent
            except:
                pass
                ##raise Exception(f"INVALID LINE IN FILE {FILE_GFF}: " + L)

def sortgff(dt, fout):
    buf, ret  = [], {t: 0 for t in ["gene", "mRNA", "exon", "CDS"]}
    for l in dt:
        cr, _, tp, a, b, _, st, fr, i, p = l
        a = int(a)
        buf.append([i, p, cr, tp, a, b, st, fr])

    gs, ms, es, cs = {}, {}, {}, {}

    for e in buf:
        if e[3] == 'gene':
            gs[e[0]] = [e, {}]

    pg = False
    if all([x.startswith('gene-') and len(x) > 5 for x in gs]):
        pg = True

    for e in buf:
        if e[3] == 'mRNA' and e[1] in gs:
            m = [e, [], [], 0, 0]
            ms[e[0]] = m
            gs[e[1]][1][e[0]] = m
    
    pm = False
    if all([x.startswith('rna-') and len(x) > 5 for x in ms]):
        pm = True

    for e in buf:
        if e[1] in ms:
            if e[3] == 'exon':
                ms[e[1]][1].append(e)
                ms[e[1]][3] += 1
            elif e[3] == 'CDS':
                ms[e[1]][2].append(e)
                ms[e[1]][4] += 1

    def to_ln(e, i, p=None):
        a = f"{e[2]}\t.\t{e[3]}\t{e[4]}\t{e[5]}\t.\t{e[6]}\t{e[7]}\t"
        b = f"ID={i}{('' if e[1] is None else ';Parent='+(e[1] if p is None else p))}\n"
        return a+b

    with open(fout, 'w') as fo:
        for gid, [g, dms] in sorted(gs.items(), key=lambda e: [e[1][0][2], e[1][0][4]]):
            ## se esse gene tem algum mRNA com >1 exon e algum cds
            if len([d for d in dms.values() if d[3] > 1 and d[4] > 0]) > 0:
                fo.write(to_ln(g, gid[5:] if pg else gid))
                ret["gene"] += 1
                for mid, [m, es, cs, _, _] in dms.items():
                    if len(es) > 0:
                        fo.write(to_ln(m, mid[4:] if pm else mid, gid[5:] if pg else gid))
                        ret["mRNA"] += 1
                        j, k = 0, 0
                        for e in es:
                            ret["exon"] += 1
                            j += 1
                            fo.write(to_ln(e, f'e{ret["gene"]}.{ret["mRNA"]}.{j}', mid[4:] if pm else mid))
                        for c in cs:
                            ret["CDS"] += 1
                            k += 1
                            fo.write(to_ln(c, f'c{ret["gene"]}.{ret["mRNA"]}.{k}', mid[4:] if pm else mid))
    return ret

def makegff(fin, fout, seqs):
    dt = clean_gff(fin, seqs)
    return sortgff(dt, fout)

def main():
    valids, _ = clean_fasta(FILE_GENOME, GENOM_OUT, 
                    GEN_RGX, MIN_CHR, MAX_CHR, MAX_CHRS, RESULTS+"invalid_stats.txt")

    outp = makegff(FILE_GFF, GFF_OUT, [x[0] for x in valids])

    ## {'gene': 45000, 'mRNA': 137721, 'exon': 2223011, 'CDS': 1772807}
    print("Seqs", len(valids), 
        "Genes", outp['gene'], "mRNA", outp['mRNA'], 
        "Exons", outp['exon'], "CDS", outp['CDS'])

status=f"{PROJECTS}/{PROJ}/results/status.txt"
open(status, "a")
if not "QINPUTPY ... ok!\n" in open(status).readlines():
    main()
else:
    print("skipping QINPUTPY last run")

print('TERMINADO_COM_SUCESSO')
open(status, "a").write("QINPUTPY ... ok!\n")
open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("E " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")