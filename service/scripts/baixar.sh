#!/bin/bash

PROJECTS=$1
PROJ=$2
ID=$3
URL=$4
PARA=$5
SRA=$6
PAIRED=$7
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
INPUTS=$PROJECTS/$PROJ/inputs

[ $SRA ] && echo $PAIRED fasterq-dump $URL -O $INPUTS 
[ ! $SRA ] && echo wget -qO $PARA $URL

[ ! $SRA ] && wget -qO $INPUTS/$PARA $URL 1> $LOG 2> $ERR  && echo TERMINADO_COM_SUCESSO

[ $SRA ] && fasterq-dump --split-3 $URL -O $INPUTS -t /tmp/geneappdata/sra 1> $LOG 2> $ERR
[ $PAIRED ] && mv $URL.1.fq $PARA.1.fq && mv $URL.2.fq $PARA.2.fq && echo TERMINADO_COM_SUCESSO