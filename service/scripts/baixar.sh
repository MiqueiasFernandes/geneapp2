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
R=$PROJECTS/$PROJ/results
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

[ $SRA ] && echo $PAIRED fasterq-dump $URL -O $INPUTS 
[ ! $SRA ] && echo wget -qO $PARA $URL

if ! grep -q $PARA $R/status.txt ; then
    [ ! $SRA ] && wget -qO $INPUTS/$PARA $URL 1> $LOG 2> $ERR  && echo TERMINADO_COM_SUCESSO

    [ $SRA ] && fasterq-dump --split-3 $URL -O $INPUTS -t /tmp/geneappdata/sra 1> $LOG 2> $ERR
    [ $SRA ] && [ ! $PAIRED ] && mv $INPUTS/$URL.fastq $INPUTS/$PARA.fq && echo TERMINADO_COM_SUCESSO
    [ $PAIRED ] && mv $INPUTS/$URL\_1.fastq $INPUTS/$PARA.1.fq && mv $INPUTS/$URL\_2.fastq $INPUTS/$PARA.2.fq && echo TERMINADO_COM_SUCESSO
else
    echo "skipping $PARA sucess get"
    echo skiped 1>> $LOG 2>> $ERR
    echo TERMINADO_COM_SUCESSO
    sleep 1
fi
echo "$PARA $(date +%d/%m\ %H:%M) file downloaded." >> $R/status.txt
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
