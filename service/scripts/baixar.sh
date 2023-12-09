#!/bin/bash

PROJECTS=$1
PROJ=$2
ID=$3
URL=$4
PARA=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo wget -qO $PARA $URL

wget -qO $PROJECTS/$PROJ/inputs/$PARA $URL 1> $LOG 2> $ERR

echo TERMINADO_COM_SUCESSO