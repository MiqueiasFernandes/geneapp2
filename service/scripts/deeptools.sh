#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG $ERR 
L=RUN_DEEPTOOLS
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
source /geneapp_env/bin/activate

if ! grep -q "$L" $R/status.txt ; then

    echo "$(date +%d/%m\ %H:%M) iniciando geracao de BEDs" >>$LOG
   
    ## gerar bed dos AS genes
    
    rm -f $R/cov_all.bed
    for SAMPLE in $(cut -d, -f2 $I/t3drnaseq_tmp/exper*.csv | tail -n+2); do
        BAM=$R/bams/$SAMPLE.idx_genes.bam
        echo $BAM ... >>$LOG
        if [ -f $BAM ]; then
            echo "Gerando BED dos genes para $SAMPLE"
            [ -f $I/cov_$SAMPLE.bed ] || (for GENE in $(cat $R/das_genes.txt); do
                bamCoverage -b $BAM -o $I/tmp.$ID.bed --outFileFormat bedgraph --binSize 3 -p 2 -r $GENE 1>>$LOG 2>>$ERR &&
                    cat $I/tmp.$ID.bed | sed s/^/$SAMPLE,/ | tr -s [:blank:] , >> $R/cov_all.bed
            done )
        fi
    done
    echo "$(date +%d/%m\ %H:%M) terminou geracao de BEDs" >>$RESUMO


else
    echo "skipping $L sucess run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) finished" >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

