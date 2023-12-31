#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
G=$4        ## genome[cleaned].fasta
A=$5        ## anotattion.gff3
X=$6        ## genes_clean.gff3
Z=$7        ## genes.fa

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
source /geneapp_env/bin/activate
echo ".... QINPUT SH ...." > $LOG
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

## fasta limpo
echo $G
## anotacao limpo
echo $A
## novo gff
echo $X
## fasta dos genes
echo $Z
L=QINPUTSH

if ! grep -q $L $R/status.txt ; then

cd $PROJECTS/$PROJ
gffread $I/$A -g $I/$G --no-pseudo -UCOo $R/$X &&
gffread $R/$X -g $I/$G -w $R/transcripts.fa -x $R/cds.fa -Sy $R/proteins.fa -To $R/genes.gtf &&
cat <<EOF | /app/scripts/_py - && echo TERMINADO_COM_SUCESSO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
x = "$I/$G"
y = "$R/$X"
print(x, y)
genes = [g.split("\t") for g in open(y) if "\tgene\t" in g]
chrs = {c: [] for c in set([g[0] for g in genes])}
for g in genes:
    chrs[g[0]].append([g[-1].split("ID=")[1].split(";")[0], int(g[3]), int(g[4]), g[6] == "+"])

ss = []
for seq in SeqIO.parse(x, "fasta"):
    if seq.id in chrs:
        SeqIO.write(seq, open("$R/genome.final.fasta", "a"), "fasta")
    else:
        continue
    for gid, start, end, strand in chrs[seq.id]:
        s = SeqRecord(seq.seq[start-1:end])
        s = s if strand else s.reverse_complement()
        s.id, s.description = gid, ""
        ss.append(s)

o = "$R/$Z"
z = SeqIO.write(ss, o, "fasta")
print(z, "genes stored at", o)

gff = [x.strip().split("\t") for x in open(y) if not x.startswith("#")]
ms = [x[-1].split(";") for x in gff if x[2] == 'mRNA']
open("$R/transcript_gene_mapping.csv", "w").writelines(["TXNAME,GENEID\n"]+[f"{t[3:]},{g[7:]}\n" for t, g in ms])
EOF
else
    echo "skipping $L sucess run"
    sleep 1
    echo TERMINADO_COM_SUCESSO
fi
echo "$L $(date +%d/%m\ %H:%M)" >> $R/status.txt
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"