#!/bin/bash

PROJECTS=$1
PROJ=$2
ID=$3
DE=$4
PARA=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
R=$PROJECTS/$PROJ/results
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

echo cp $PROJECTS/inputs/$DE $PROJECTS/$PROJ/inputs/$PARA

if ! grep -q $PARA $R/status.txt ; then
    cp $PROJECTS/inputs/$DE $PROJECTS/$PROJ/inputs/$PARA 1> $LOG 2> $ERR && echo TERMINADO_COM_SUCESSO
else
    echo "skipping $PARA sucess get"
    echo skiped 1>> $LOG 2>> $ERR
    echo TERMINADO_COM_SUCESSO
    sleep 1
fi

echo "$PARA $(date +%d/%m\ %H:%M) file copied." >> $R/status.txt
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"