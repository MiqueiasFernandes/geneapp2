#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
SAMPLE=$4   ## SRR34534534
PARAM=$5    ## ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True LEADING:3 TRAILING:3 MINLEN:36
IS_PE=$6    ## 1 => PE
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
RUN=$I/$SAMPLE
L=SMP.$SAMPLE-$IS_PE.QC

echo ".... QC SAMPLE $IS_PE ...." > $LOG 
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
echo $IS_PE $SAMPLE 
echo $PARAM

if ! grep -q $L $R/status.txt ; then
    if [ $IS_PE ]; then
        echo "fazendo controle de qualidade da amostra $SAMPLE com o TrimmomaticPE ..."

        [ ! -f "$RUN.1.fq" ] && echo ERRO sample fastq $RUN.1.fq NOT FOUND > $ERR && exit 1
        [ ! -f "$RUN.2.fq" ] && echo ERRO sample fastq $RUN.2.fq NOT FOUND > $ERR && exit 1

        TrimmomaticPE \
            $RUN.1.fq $RUN.2.fq \
            $I/$SAMPLE.F.fq $I/$SAMPLE.1.unp.fq \
            $I/$SAMPLE.R.fq $I/$SAMPLE.2.unp.fq \
            $PARAM 1>> $LOG 2>> $ERR && \
        rm $RUN.1.fq $RUN.2.fq $I/$SAMPLE.1.unp.fq $I/$SAMPLE.2.unp.fq
    else
        echo "fazendo controle de qualidade da amostra $SAMPLE com o TrimmomaticSE ..."
        [ ! -f "$RUN.fq" ] && echo ERRO sample fastq $RUN.fq NOT FOUND > $ERR && exit 1
        TrimmomaticSE \
            $RUN.fq $I/cln_$SAMPLE.fq \
            $PARAM 1>> $LOG 2>> $ERR  && \
        rm $RUN.fq
    fi

    grep 'Surviving' $ERR | sed "s/^/$SAMPLE,/"

    ## samples clean =>   $SAMPLE.F.fq    $SAMPLE.R.fq    cln_$SAMPLE.fq

    # # 3 rodar o fastqc
    echo "reportando controle de qualidade da amostra $RUN com fastqc ..."
    rm -rf $R/qc_$SAMPLE && mkdir $R/qc_$SAMPLE
    if [ $IS_PE ]; then
        fastqc $I/$SAMPLE.F.fq $I/$SAMPLE.R.fq -o $R/qc_$SAMPLE 1>> $LOG 2>> $ERR
    else
        fastqc $I/cln_$SAMPLE.fq -o $R/qc_$SAMPLE 1>> $LOG 2>> $ERR
    fi
else
    echo "skipping $L sucess run"
    sleep 1
fi
echo "$L $(date +%d/%m\ %H:%M) sample processed." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
