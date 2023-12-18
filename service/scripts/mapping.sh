#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
SAMPLE=$4   ## SRR34534534
INDEX=$5    ## idx_genome
PARAM=$6    ## --no-unal
IS_PE=$7    ## 1 => PE
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
IDX_DIR=$I/idxs/$INDEX
echo "INDEX DIR => $IDX_DIR"
RUN=$I/$SAMPLE
[ ! "$IS_PE" ] && RUN=$I/cln_$SAMPLE
L=SMP.$SAMPLE-$IS_PE.MP.$INDEX

echo ".... MAPPING $SAMPLE $IS_PE $IDX_DIR ...." > $LOG 
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
echo $IS_PE $SAMPLE 
echo $PARAM

SAM=$I/$SAMPLE.$INDEX.maped.sam

[ ! -d "$R/bams" ] && mkdir $R/bams

if ! grep -q "$L" $R/status.txt ; then
    echo "mapeando $SAMPLE $IS_PE com hisat2 em $IDX_DIR ."
    if [ $IS_PE ]; then
        hisat2 -x $IDX_DIR -1 $RUN.F.fq -2 $RUN.R.fq $PARAM -S $SAM \
            1>>$LOG 2>>$ERR
    else
        hisat2 -x $IDX_DIR -U $RUN.fq $PARAM -S $SAM \
            1>>$LOG 2>>$ERR
    fi

    if [ -f $SAM ]; then
        echo "gerando bam de $SAM para sorted bam"
        samtools view -S -b $SAM >$I/$SAMPLE.maped.$INDEX.tmp.bam 2>>$ERR
        bamtools sort -in $I/$SAMPLE.maped.$INDEX.tmp.bam -out $R/bams/$SAMPLE.$INDEX.bam 1>>$LOG 2>>$ERR
        rm -rf $SAM $I/$SAMPLE.maped.$INDEX.tmp.bam
    fi
else
    echo "skipping $L sucess mapping run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) sample mapped." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
