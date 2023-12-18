#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
SAMPLE=$4   ## SRR34534534
INDEX=$5    ## idx_genome_slm
PARAM=$6    ## --libType IU
IS_PE=$7    ## 1 => PE
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
IDX_DIR=$I/idxs/$INDEX
echo "INDEX DIR => $IDX_DIR"
RUN=$I/$SAMPLE
[ ! "$IS_PE" ] && RUN=$I/cln_$SAMPLE
L=SMP.$SAMPLE-$IS_PE.QT.$INDEX

echo ".... QUANTIFY $SAMPLE $IS_PE $IDX_DIR ...." > $LOG 
touch $ERR
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
echo $IS_PE $SAMPLE 
echo $PARAM
[ ! -d "$R/quants" ] && mkdir $R/quants

if ! grep -q "$L" $R/status.txt ; then

    # 7 quantificar com salmon
    echo "quantificando com a amostra $SAMPLE com salmon"
    if [ $IS_PE ]; then
        salmon quant $PARAM -1 $RUN.F.fq -2 $RUN.R.fq -o $I/quant_$SAMPLE --index $IDX_DIR \
            1>>$LOG 2>>$ERR
    else
        salmon quant $PARAM -r $RUN.fq -o $I/quant_$SAMPLE --index $IDX_DIR \
            1>>$LOG 2>>$ERR
    fi
    cp $I/quant_$SAMPLE/quant.sf $R/quants/$SAMPLE.quant.sf
    echo "$(date +%d/%m\ %H:%M) mRNAS expressa em $SAMPLE: $(cut -f4 $R/quants/$SAMPLE.quant.sf | tail -n+2 | grep -cv '^0$')" 

else
    echo "skipping $L sucess quantify run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) sample mapped." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
