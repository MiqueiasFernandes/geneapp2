#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
G=$4        ## genome.fasta
O=$5        ## idxgenoma
S=$6        ## 1 = is salmon
ARGS=$7

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo ".... INDEX FASTA $S ...." > $LOG  && touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
IDX_DIR=$I/idxs
[ ! -d "$IDX_DIR" ] && mkdir $IDX_DIR
echo "INDEX DIR => $IDX_DIR"
echo "ARGS => " $ARGS

if ! grep -q $O $R/status.txt ; then
    if [ $S ]; then
        echo  "indexing $G to quantify => SALMON"
        salmon index -t $R/$G --index $IDX_DIR/$O $ARGS 1>$LOG 2>$ERR
    else
        echo  "indexing $G to mapping => HISAT2"
        hisat2-build $R/$G $IDX_DIR/$O $ARGS 1>$LOG 2>$ERR
    fi
else
    echo "skipping $O sucess run"
    sleep 1
fi
echo "$O $(date +%d/%m\ %H:%M) indexing end." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"