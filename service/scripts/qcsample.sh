#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
SAMPLE=$4   ## SRR34534534
IS_PE=$5    ## 1 => PE
PARAM=$6    ## ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True LEADING:3 TRAILING:3 MINLEN:36
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
RUN=$I/$SAMPLE

echo ".... QC SAMPLE ...." > $LOG  && touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
echo $IS_PE $SAMPLE 
echo $PARAM

# # 2 controle de qualidade
if [ $IS_PE ]; then
    echo "fazendo controle de qualidade da amostra $SAMPLE com o TrimmomaticPE ..."
    TrimmomaticPE \
        $RUN.1.fq $RUN.2.fq \
        $I/$SAMPLE.F.fq $I/$SAMPLE.1.unp.fq \
        $I/$SAMPLE.R.fq $I/$SAMPLE.2.unp.fq \
        $PARAM 1>$LOG 2>$ERR
    rm $RUN.1.fq $RUN.2.fq $I/$SAMPLE.1.unp.fq $I/$SAMPLE.2.unp.fq
else
    echo "fazendo controle de qualidade da amostra $SAMPLE com o TrimmomaticSE ..."
    TrimmomaticSE \
        $RUN.fq $I/$SAMPLE.fq \
        $PARAM 1>$LOG 2>$ERR
    rm $RUN.fq
fi
grep 'Surviving' $LOG_DIR/_5.$SID.2_qc.$SAMPLE.err.txt | sed "s/^/$SAMPLE,/"

# # 3 rodar o fastqc
echo "reportando controle de qualidade da amostra $SAMPLE com fastqc ..."
rm -rf qc_$SAMPLE && mkdir qc_$SAMPLE
if [ $IS_PE ]; then
    fastqc $SAMPLE.F.fq $SAMPLE.R.fq -o qc_$SAMPLE 1>$LOG 2>$ERR
else
    fastqc $SAMPLE.fq -o qc_$SAMPLE 1>$LOG 2>$ERR
fi

echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
