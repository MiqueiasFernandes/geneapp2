PROJECTS=$1
ID=$2
PROJ=$3
URL=$4
PARA=$5
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo wget -qO $PARA $URL 1> $LOG 2> $ERR
wget -qO $PARA $URL 1>> $LOG 2>> $ERR
echo sucesso 1>> $LOG 2>> $ERR