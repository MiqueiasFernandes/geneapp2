#!/bin/bash

PROJECTS=$1
PROJ=$2
ID=$3
DE=$4
PARA=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo cp $PROJECTS/inputs/$DE $PROJECTS/$PROJ/inputs/$PARA

cp $PROJECTS/inputs/$DE $PROJECTS/$PROJ/inputs/$PARA 1> $LOG 2> $ERR && echo TERMINADO_COM_SUCESSO