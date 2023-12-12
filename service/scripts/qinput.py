#!/bin/python3
import sys
from pathlib import Path
import re
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

## genome.fasta => anotattion.gff3 => transcriptome.fna => proteome.faa
GN=sys.argv[4]
GENOM=INPUTS+GN
AN=sys.argv[5]
ANOT=INPUTS+AN
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
log(f'#{len(seqs)} found in fasta {GENOM}')

print("validando genoma ...")

CGENOM=INPUTS+"cln_"+GN

valid_seqs, invalid_seqs, tam = [], [], 0
seq_id, buf, valid = None, [], True
map_seqs = {}
map_nn = {}
sizes = {}
GENOM_STR = re.compile(r"^[actgnrykmswbdhvACTGNRYKMSWBDHV]+$")
open(CGENOM, 'w').write('')
for line in open(GENOM):
    if line.startswith('>'):
        name = line.strip()[1:].split(' ')[0]
        if name in sizes:
            err("SEQ " + name + " DUPLICATED NAME IN FILE "+GENOM)
            exit(1)
        if seq_id is None:
            seq_id = name
            valid = len(seq_id) > 1
        else:
            if valid and (not tam > MIN_SEQ):
                err("Seq "+ seq_id+ " invalid size => "+ str(tam))
            valid = tam > MIN_SEQ
            sizes[seq_id] = tam
            if valid:
                valid_seqs.append(seq_id)
                nn = f'Chr{str(len(valid_seqs)).rjust(2, "0")}'
                map_seqs[seq_id] = nn
                map_nn[nn] = seq_id
                open(CGENOM, 'a').writelines([">"+nn+"\n"]+buf)
            else:
                invalid_seqs.append(seq_id)
            buf = []
            seq_id = name
            valid = len(seq_id) > 1
            tam = 0
    elif valid:
        x = line.strip()
        if re.fullmatch(GENOM_STR, x):
            buf.append(x + '\n')
            tam += len(x)
        else:
            err("Seq "+ seq_id +" invalid => " +line)
            valid = False

if valid and tam > MIN_SEQ:
    valid_seqs.append(seq_id)
    nn = f'Chr{str(len(valid_seqs)).rjust(2, "0")}'
    map_seqs[seq_id] = nn
    map_nn[nn] = seq_id
    sizes[seq_id] = tam
    open(CGENOM, 'a').writelines([">"+nn+"\n"]+buf)
else:
    invalid_seqs.append(seq_id)

if len(invalid_seqs) > 0:
    err("INVALID SEQS:" + ", ".join(invalid_seqs))

if len(valid_seqs) < 1:
    err("NOT SEQ VALIDA FOUND")
    exit(1)
    
tt_size = 0
gs=INPUTS+GN+".stats.txt"

with open(gs, 'w') as fo:
    for seq, s in sizes.items():
        if seq in valid_seqs:
            tt_size += s
            fo.write(f"{map_seqs[seq]}\t{s}\t{seq}\n")

if tt_size > MIN_SEQ*10000:
    err(f"GENOM TOO BIGGER {tt_size}")
    exit(1)

print(len(valid_seqs), "VALID SEQS")
print(f"GENOME total size {tt_size} base pairs.")

def get_entry(gff, seq, t="gene"):
    chrm = seq+"\t"
    raw = [x.strip().split('\t')[:9] for x in open(gff) if x.startswith(chrm)]
    valid = [x for x in raw if x[2] == t and len(x) == 9]
    loc = [[seq if t == 'gene' else d.split("Parent=")[1].split(";")[0],
            d.split("ID=")[1].split(";")[0],c,a,b,x] for _,_,_,a,b,_,c,x,d in valid]
    return loc

def valid_regs(gff, chrm):

        def validator(pai, id, strand, start, end, phase):
                try:
                        if (not start.isdigit()) or (not end.isdigit()):
                                return False 
                        a, b = int(start), int(end)
                        assert a > 0 and b > a
                        assert strand == "+" or strand == "-"
                except:
                        return False
                return len(pai.strip()) > 1 and len(id.strip()) > 1 and phase in ['.' ,'0', '1', '2']

        _genes = [x for x in get_entry(gff, chrm)]
        _mrnas = [x for x in get_entry(gff, chrm, "mRNA")]
        _exons = [x for x in get_entry(gff, chrm, "exon")]
        _cds = [x for x in get_entry(gff, chrm, "CDS")]

        genes = [x for x in _genes if validator(*x)]
        mrnas = [x for x in _mrnas if validator(*x)]
        exons = [x for x in _exons if validator(*x)]
        cds = [x for x in _cds if validator(*x)]

        mrna_cds = set([x[0] for x in cds])
        mrna_exons = set([x[0] for x in exons])
        vmrnas = mrna_cds.intersection(mrna_exons)
        mids = set([x[1] for x in mrnas]).intersection(vmrnas)
        gids = set([x[1] for x in genes])

        vmids = [x[1] for x in mrnas if x[0] in gids and x[1] in mids]

        clean_cds = [x for x in cds if x[0] in vmids]
        clean_exon = [x for x in exons if x[0] in vmids]
        clean_mrna = [x for x in mrnas if x[1] in vmids]
        vgids = set([x[0] for x in clean_mrna])
        clean_gene = [x for x in genes if x[1] in vgids]

        _c = set([x[1] for x in clean_cds])
        mcds_err = set([x[0] for x in cds if not x[1] in _c])
        _e = set([x[1] for x in clean_exon])
        mexon_err = set([x[0] for x in exons if not x[1] in _e])
        merr = mcds_err.union(mexon_err)
        gerr = [x[0] for x in clean_mrna if x[1] in merr]

        gene_ok = [g for g in clean_gene if not g[1] in gerr]
        mrna_ok = [m for m in clean_mrna if not m[0] in gerr]
        mids = set([x[1] for x in mrna_ok])
        exon_ok = [e for e in clean_exon if e[0] in mids]
        cds_ok = [c for c in clean_cds if c[0] in mids]

        inv = len(_genes)-len(gene_ok), len(_mrnas)-len(mrna_ok), len(_exons)-len(exon_ok), len(_cds)-len(cds_ok)

        return clean_gene, clean_mrna, clean_exon, clean_cds, inv

def regorg(genes, mrnas, exons, cds):
        
        ms_g = {x[1]: [] for x in genes}
        for m in mrnas:
              ms_g[m[0]].append(m)

        es_m = {x[1]: [] for x in mrnas}
        for e in exons:
              es_m[e[0]].append(e)

        cs_m = {x[1]: [] for x in mrnas}
        for c in cds:
              cs_m[c[0]].append(c)

        for seq, gene, strand, start, end, phase in genes:
                yield 'gene', gene, seq, strand, start, end, phase
                for gid, mrna, strand, start, end, phase in ms_g[gene]:
                        yield 'mRNA', mrna, gid, strand, start, end, phase
                        for mid, exon, strand, start, end, phase in es_m[mrna]:
                                yield 'exon', exon, mid, strand, start, end, phase
                        for mid, icds, strand, start, end, phase in cs_m[mrna]:
                                yield 'CDS', icds, mid, strand, start, end, phase
                                
def rename(seq, gff, cg=1):
        dt, mapx, cm, ce, cc = [], {}, 0, 0, 0
        for t,id,parent,strand,start,end,frame in gff:
                if t == 'gene':
                        x = f'gene{str(cg).rjust(4, "0")}'
                        cg += 1
                        mapx[id] = x
                        dt.append([seq, '', 'gene', start, end, '', strand,frame,"ID="+x])
                        cm, ce, cc = 0, 0, 0
                elif t == 'mRNA':
                        cm += 1
                        x = f'{mapx[parent]}m{str(cm).rjust(2, "0")}'
                        mapx[id] = x
                        dt.append([seq, '', 'mRNA', start, end, '', strand,frame,f"ID={x};Parent={mapx[parent]}"])
                elif t == 'exon':
                        ce += 1
                        x = f'{mapx[parent]}e{str(ce).rjust(2, "0")}'
                        mapx[id] = x
                        dt.append([seq, '', 'exon', start, end, '', strand,frame,f"ID={x};Parent={mapx[parent]}"])
                elif t == 'CDS':
                        cc += 1
                        x = f'{mapx[parent]}c{str(cc).rjust(2, "0")}'
                        mapx[id] = x
                        dt.append([seq, '', 'CDS', start, end, '', strand,frame,f"ID={x};Parent={mapx[parent]}"])
        return dt, mapx
          
def clean_gff(gff, seqs_map, gout, mout):
        invs, gcount, emap = [], 1, {}
        with open(gout, 'w') as fo:
                for seq, nseq in seqs_map.items():
                        genes, mrnas, exons, cds, inv = valid_regs(gff, seq)
                        invs.append([nseq, seq, list(map(len, [genes, mrnas, exons, cds])), inv])
                        rg = list(regorg(genes, mrnas, exons, cds))
                        ng, mx = rename(nseq, rg, gcount)
                        gcount = len(genes)+1
                        emap.update(mx)
                        for l in ng:
                                fo.write("\t".join(l)+"\n")
        with open(mout, 'w') as fo:
                for k, v in emap.items():
                        fo.write(f"{v}\t{k}\n")
        return invs

seqs = {x[2]: x[0] for x in [x.strip().split("\t") for x in open(gs)]}
cln_anot = clean_gff(ANOT, seqs, INPUTS+AN+".genes.gff3", INPUTS+AN+".gene_rename.txt")
seqs_vz = [x[0] for x in cln_anot if x[2][0] < MIN_G_SEQ]
seqs = [x[1] for x in sorted([(int(b), a) for a, b, _ in [x.split('\t') for x in open(gs)]], key=lambda e: -e[0])]
seq_ir = [x for x in seqs if not x in seqs_vz]

print(len(seq_ir), "Valid seqs", seq_ir)

if len(seqs_vz) > 0:
    err(f"SEQ HAS NO GENES: " + ", ".join(seqs_vz))

if len(seq_ir) < 1:
    err(f"GENOM HAS NO annotated seqs.")
    exit(1)

for s in seq_ir:
    for seq in SeqIO.parse(CGENOM, "fasta"):
        if seq.id == s:
            with open(INPUTS+GN+'.genome.fa', 'a') as fw:
                SeqIO.write(seq, fw, "fasta")

gs, ms, es, cs = 0, 0, 0, 0
with open(INPUTS+GN+".data_quality.csv", "w") as fo:
    fo.write("Chr;Seq;Genes;mRNAs;Exons;CDS;invG;invM;invE;invC\n")
    for (a,b,(c,d,e,f),(g,h,i,j)) in cln_anot:
        fo.write(";".join(list(map(str,[a,b,c,d,e,f,g,h,i,j])))+"\n")
        gs += c
        ms += d
        es += e
        cs += f

print("Seqs", len(seq_ir), "Genes", gs, "mRNA", ms, "Exons", es, "CDS", cs)




print('TERMINADO_COM_SUCESSO')

open(f"{PROJECTS}/{PROJ}/jobs/jobs.txt", "a").write("E " + ID + " "+ datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()+"\n")