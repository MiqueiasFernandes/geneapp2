#!/bin/bash

PROJECTS=$1
PROJ=$2
ID=$3
F=$4
MSG=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

echo show $F '=>' $MSG
echo $MSG > $PROJECTS/$PROJ/results/$F
touch $LOG
touch $ERR
echo TERMINADO_COM_SUCESSO

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"