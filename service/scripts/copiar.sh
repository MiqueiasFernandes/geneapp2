PROJECTS=$1
ID=$2
PROJ=$3
DE=$4
PARA=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo cp $DE $PARA 1> $LOG 2> $ERR
cp $DE $PARA 1>> $LOG 2>> $ERR
echo sucesso 1>> $LOG 2>> $ERR