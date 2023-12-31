#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
G=$4        ## genome.fasta
A=$5        ## 1
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo ".... JOINX ...." > $LOG
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

cd $PROJECTS/$PROJ
source /app/flask_env/bin/activate

OG=$R/genome.fa
OA=$I/genes.gff3

cat $I/$G\_pt*.genome.fa > $OG && 
cat $I/$G\_pt*.data_quality.csv > $R/data_quality.csv && 
cat $I/$G\_pt*.stats.txt > $R/stats.txt && 
cat $I/$A\_pt*.genes.gff3 > $OA && 
cat $I/$A\_pt*.gene_rename.txt > $R/gene_rename.txt && 
cat <<EOF | python3 - && echo TERMINADO_COM_SUCESSO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

x = "$OG"
y = "$OA"
print(x, y)

genes = [g.split("\t") for g in open(y) if "\tgene\t" in g]
chrs = {c: [] for c in set([g[0] for g in genes])}
for g in genes:
    chrs[g[0]].append([g[-1].split("ID=")[1].split(";")[0].strip(), int(g[3]), int(g[4]), g[6] == "+"])

ss = []
for seq in SeqIO.parse(x, "fasta"):
    for gid, start, end, strand in chrs[seq.id]:
        s = SeqRecord(seq.seq[start-1:end])
        s = s if strand else s.reverse_complement()
        s.id, s.description = gid, ""
        ss.append(s)
o = "$R/genes.fa"
z = SeqIO.write(ss, o, "fasta")
print(z, "genes stored at", o)
EOF

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"