#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG $ERR 
SERVER="https://www.genome.jp/tools-bin/ete"
L=RUN_ETE3

if ! grep -q "$L" $R/status.txt ; then

    echo "Running ETE3 on $SERVER ..."
    # cd $TMP_DIR
    # local A_SEQ=$TMP_DIR/das_genes.fna
    # local A_FILO=$OUT_DIR/filogenia.txt
    # local J_FILO=$TMP_DIR/geneapp/job_filogenia.txt

    # python3 <(printf "
    #     from Bio import SeqIO
    #     gene_seqs = SeqIO.parse('$TMP_DIR/gene_seqs.fa' , 'fasta')
    #     gene_as = set([l.strip() for l in open('$TMP_DIR/geneapp/all_as_genes.txt') if len(l) > 2])
    #     SeqIO.write([x for x in gene_seqs if x.id in gene_as], '$A_SEQ', 'fasta')
    # " | cut -c9-) 1>$LOG_DIR/_6.4.0_ext_genes.log.txt 2>$LOG_DIR/_6.4.0_ext_genes.err.txt

    # if [ -f $A_FILO ]; then
    #     echo "$(date +%d/%m\ %H:%M) recuperando filogenia de $A_FILO" >>$RESUMO
    #     return
    # fi

    # if [ -f $J_FILO ]; then
    #     JOB=$(head -1 $J_FILO | tr -d :alphanum:)
    #     echo "$(date +%d/%m\ %H:%M) recuperando filogenia em $JOB" >>$RESUMO
    # else
    #     echo "gerando job" 1>>$LOG_DIR/_6.5.1_filogeny.log.txt
    #     SEQ=${2:-"nucleotide"}              #  protein
    #     workflow1=${3:-"mafft_default"}     #  mafft_einsi   mafft_linsi mafft_ginsi  clustalo_default  muscle_default
    #     workflow2=${4:-"-none"}             # -trimal001 -trimal01 -trimal02 -trimal05  -trimal_gappyout
    #     workflow3=${5:-"-none"}             # -prottest_default  -pmodeltest_full_ultrafast  -pmodeltest_full_fast  -pmodeltest_full_slow  -pmodeltest_soft_ultrafast  -pmodeltest_soft_fast -pmodeltest_soft_slow
    #     workflow4=${6:-"-fasttree_default"} # -bionj_default  -fasttree_default  -fasttree_full  -phyml_default  -phyml_default_bootstrap  -raxml_default  -raxml_default_bootstrap

    #     DATA="upload_file=@$A_SEQ" #DATA="sequence=`cat $FILE`"

    #     JOB=$(curl -s \
    #         -F "seqtype=$SEQ" \
    #         -F "seqformat=unaligned" \
    #         -F "$DATA" \
    #         -F "workflow1=$workflow1" \
    #         -F "workflow2=$workflow2" \
    #         -F "workflow3=$workflow3" \
    #         -F "workflow4=$workflow4" \
    #         -F "workflow=$workflow1$workflow2$workflow3$workflow4" $SERVER | grep -m1 'ete?id=' | cut -d= -f2 | cut -d\" -f1)

    #     echo $JOB >$J_FILO
    #     echo "$(date +%d/%m\ %H:%M) rodando filogenia em $JOB" >>$RESUMO
    # fi

    # if (($(echo $JOB | awk '{print length}') > 10)); then
    #     while (($(curl -s $SERVER'?id='$JOB | grep -c "Your job is still running") > 0)); do
    #         echo aguardando ... 1>>$LOG_DIR/_6.5.1_filogeny.log.txt
    #         sleep $TIMEOUT
    #     done
    #     echo terminou 1>>$LOG_DIR/_6.5.1_filogeny.log.txt
    #     curl -s $SERVER'?id='$JOB | grep -m1 midpoint_data | cut -d\" -f2 >$A_FILO
    # else
    #     echo "job $JOB falhou" 2>>$LOG_DIR/_6.5.1_filogeny.err.txt
    # fi
    # echo "filogenia terminou $JOB" 1>>$LOG_DIR/_6.5.1_filogeny.log.txt
    # echo "$(date +%d/%m\ %H:%M) terminou filogenia" >>$RESUMO













else
    echo "skipping $L sucess run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) finished." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"


