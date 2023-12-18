#!/bin/bash

PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99

PS1=$4   
PS2=$5   
PS3=$6   
PS4=$7   
PS5=$8   
PS6=$9  
PS7=${10}  
PS8=${11}  
PS9=${12}  
PS10=${13}   

LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo ".... HOLDER ...." > $LOG
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

cd $PROJECTS/$PROJ

##X=`tsp -p $PS1` && echo pid $X  &&  tail --pid=$X -f /dev/null

[ $PS1 ] && echo "waiting for $PS1 ..." && tsp -w $PS1
[ $PS2 ] && echo "waiting for $PS2 ..." && tsp -w $PS2
[ $PS3 ] && echo "waiting for $PS3 ..." && tsp -w $PS3
[ $PS4 ] && echo "waiting for $PS4 ..." && tsp -w $PS4
[ $PS5 ] && echo "waiting for $PS5 ..." && tsp -w $PS5
[ $PS6 ] && echo "waiting for $PS6 ..." && tsp -w $PS6
[ $PS7 ] && echo "waiting for $PS7 ..." && tsp -w $PS7
[ $PS8 ] && echo "waiting for $PS8 ..." && tsp -w $PS8
[ $PS9 ] && echo "waiting for $PS9 ..." && tsp -w $PS9
[ $PS10 ] && echo "waiting for $PS10 ..." && tsp -w $PS10

echo TERMINADO_COM_SUCESSO

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
