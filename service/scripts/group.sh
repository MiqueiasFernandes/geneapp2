#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99

##ARG1=$4
##ARG2=$5
##ARG3=$6
##ARG4=$7
##ARG5=$8
##ARG6=$9

TIMEOUT=10
I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG $ERR 
SERVER="https://www.genome.jp/tools-bin/ete"
L=RUN_ETE3
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
if ! grep -q "$L" $R/status.txt ; then

    echo "Running ETE3 on $SERVER ($TIMEOUT s) ..."
    TMP_DIR=$I/ete3
    rm -rf $TMP_DIR && mkdir $TMP_DIR && cd $TMP_DIR
    A_SEQ=$R/das_genes.fa
    A_FILO=$R/filogenia.txt
    J_FILO=$TMP_DIR/job_filogenia.txt

    if [ ! -f $J_FILO ]; then

        echo "gerando job para `grep -c \> $A_SEQ` genes..."
        SEQ=${4:-"nucleotide"}              #  protein
        workflow1=${5:-"mafft_default"}     #  mafft_einsi   mafft_linsi mafft_ginsi  clustalo_default  muscle_default
        workflow2=${6:-"-none"}             # -trimal001 -trimal01 -trimal02 -trimal05  -trimal_gappyout
        workflow3=${7:-"-none"}             # -prottest_default  -pmodeltest_full_ultrafast  -pmodeltest_full_fast  -pmodeltest_full_slow  -pmodeltest_soft_ultrafast  -pmodeltest_soft_fast -pmodeltest_soft_slow
        workflow4=${8:-"-fasttree_default"} # -bionj_default  -fasttree_default  -fasttree_full  -phyml_default  -phyml_default_bootstrap  -raxml_default  -raxml_default_bootstrap

        JOB=$(curl -s \
            -F "seqtype=$SEQ" \
            -F "seqformat=unaligned" \
            -F "upload_file=@$A_SEQ" \
            -F "workflow1=$workflow1" \
            -F "workflow2=$workflow2" \
            -F "workflow3=$workflow3" \
            -F "workflow4=$workflow4" \
            -F "workflow=$workflow1$workflow2$workflow3$workflow4" $SERVER | grep -m1 'ete?id=' | cut -d= -f2 | cut -d\" -f1)

        echo $JOB >$J_FILO
        echo "$(date +%d/%m\ %H:%M) running filogenia on $JOB" 

    else
        JOB=$(head -1 $J_FILO | tr -d :alphanum:)
        echo "$(date +%d/%m\ %H:%M) restored filogenia on $JOB"
    fi

    echo "AGUARDANDO: $JOB ..."
   
    if (($(echo $JOB | awk '{print length}') > 10)); then
        while (($(curl -s $SERVER'?id='$JOB | grep -c "Your job is still running") > 0)); do
            echo aguardando ... >> $LOG
            sleep $TIMEOUT
        done
        echo terminou ...
        curl -s $SERVER'?id='$JOB | grep -m1 midpoint_data | cut -d\" -f2 >$A_FILO
        echo "$L $(date +%d/%m\ %H:%M) finished." >> $R/status.txt
    else
        echo "job $JOB falhou" >> $ERR
    fi
    echo "$(date +%d/%m\ %H:%M) terminou filogenia no job $JOB"
else
    echo "skipping $L sucess run"
    sleep 1
fi

echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
