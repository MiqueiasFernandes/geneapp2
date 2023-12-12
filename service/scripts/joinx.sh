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

cat $I/$G\_pt*.genome.fa > $R/genome.fa && \
cat $I/$G\_pt*.data_quality.csv > $R/data_quality.csv && \
cat $I/$G\_pt*.stats.txt > $R/stats.txt && \
cat $I/$A\_pt*.genes.gff3 > $R/genes.gff3 && \
echo TERMINADO_COM_SUCESSO

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"