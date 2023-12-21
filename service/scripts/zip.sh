#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
X=$4        ## results
M=$5        ## 1

LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

L=ZIP.$M.$X
echo "$L $(date +%d/%m\ %H:%M) file copied." >> $R/status.txt

if ! grep -q $L $R/status.txt ; then

    cd $PROJECTS/$PROJ

    [ ! $M ] && echo INFLAR $X
    [ $M ] && echo COMPRIMIR $X

    ## decompress
    [ ! $M ] && cd inputs
    [ ! $M ] && tar -tf $X && echo UNTARGZ && HANDLE=1 && tar -xvf $X 1> $LOG 2> $ERR
    [ ! $M ] && [ ! $HANDLE ] && gunzip -t $X && echo GUNZIP && HANDLE=1 && mv $X $X.gz && gunzip $X.gz 1> $LOG 2> $ERR ### not working for local
    [ ! $M ] && [ ! $HANDLE ] && unzip -t $X && echo UNZIP && HANDLE=1 && unzip $X 1> $LOG 2> $ERR    ### not working

    ## compress
    [ $M ] && ([ -f $X ] || [ -d $X ]) && echo TAR && HANDLE=1 && tar -cvf $X.tar.gz $X 1> $LOG 2> $ERR && cp $X.tar.gz results
    ##[ $M ] && [ -f $X ] && [ ! $HANDLE ] && echo GZIP && HANDLE=1 && gzip -k $X 1> $LOG 2> $ERR ## mac not works

    [ $HANDLE ] && echo TERMINADO_COM_SUCESSO
    [ ! $HANDLE ] && echo TERMINADO_COM_ERRO

else
    echo "skipping $PARA sucess get"
    echo skiped 1>> $LOG 2>> $ERR
    echo TERMINADO_COM_SUCESSO
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) file copied." >> $R/status.txt

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"