#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
EMAIL=${4:-"email@here"}

TIMEOUT=100

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG $ERR 
SERVER=https://www.ebi.ac.uk/Tools/services/rest/iprscan5/
L=RUN_INTERPRO
echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"

anotar_api() {

    OUT=$1
    PTNAS=$2
    P=$3
    Q='goterms=true&pathways=true&appl=PfamA'
    echo THREAD $P started.... >>$LOG
    sleep $P
    while read l; do
        local ID=$(echo $l | cut -d, -f1)
        local SEQ=$(echo $l | cut -d, -f2 | tr -cd '[:alpha:]')

        if grep -q "$ID" $I/interpro.txt ; then
            echo skipping $ID ...
        else
            JOB=$( curl \
                    -sSX POST \
                    --header 'Content-Type: application/x-www-form-urlencoded' \
                    --header 'Accept: text/plain' \
                    -d "email=$EMAIL&$Q&title=$ID&sequence=$SEQ" $SERVER/run)

            echo $JOB >>$LOG

            sleep 30s
            for i in $(seq $TIMEOUT); do
                if grep FINISHED <(curl -sSX GET --header 'Accept: text/plain' "$SERVER/status/$JOB") >/dev/null; then
                    curl -sSX GET --header 'Accept: text/tab-separated-values' $SERVER/result/$JOB/tsv | sed "s/^/$ID\\t/" >>$OUT
                    echo "anotacao de $ID obtida pelo job $JOB ok" >>$LOG
                    OK=1
                    echo $ID >>$I/interpro.txt
                    break
                else
                    sleep 30s
                fi
            done
            [ ! "$OK" ] && echo "Falhou " >>$ERR
        fi
    done <$PTNAS
    echo THREAD $P ended.... >>$LOG
}

if ! grep -q "$L" $R/status.txt ; then

    echo "Running INTERPROSCAN5 on $SERVER ..."

    LOCAL=$I/interpro
    FAALINES=$R/das_ptnas.inline.fa
    TSV=$R/interpro.tsv
    touch $I/interpro.txt

    if (($(grep -c , $FAALINES) > 9)); then
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f1 | grep ,) 1 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f2 | grep ,) 2 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f3 | grep ,) 3 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f4 | grep ,) 4 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f5 | grep ,) 5 &

        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f6 | grep ,) 6 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f7 | grep ,) 7 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f8 | grep ,) 8 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f9 | grep ,) 9 &
        anotar_api $TSV <(cat $FAALINES | paste - - - - - - - - - - | cut -f10 | grep ,) 0 &
        wait
        echo "anotou interpro ONLINE"
    else
        anotar_api $TSV $FAALINES 1
    fi


    echo "$(date +%d/%m\ %H:%M) terminou anotacao" >>$LOG

else
    echo "skipping $L sucess run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) finished" >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
