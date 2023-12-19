#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG $ERR 
SERVER='https://www.ebi.ac.uk/Tools/services/rest/iprscan5/'
L=RUN_INTERPRO

if ! grep -q "$L" $R/status.txt ; then

    echo "Running INTERPROSCAN5 on $SERVER ..."

# anotar() {
#     cd $TMP_DIR
#     ## anotar as ptna

#     local LOCAL=$OUT_DIR/anotacao
#     local PTNAS=$TMP_DIR/ptnas.inline
#     local TSV=$TMP_DIR/geneapp/anotacao.tsv
#     local Q='goterms=true&pathways=true&appl=PfamA'
#     echo "$(date +%d/%m\ %H:%M) iniciando anotacao" >>$RESUMO

#     log 6 4 0 "extrair ptnas das cds"

#     if [ $GEN_NCBI_TABLE ]; then
#         cat <(echo "gene,mrna,cds,protein") \
#             <(paste -d, \
#                 <(grep \> $TMP_DIR/cds.fa | sed 's/.*\[locus_tag=//' | cut -d] -f1) \
#                 <(grep \> $TMP_DIR/cds.fa | cut -d\| -f2 | sed 's/.*/\?/') \
#                 <(grep \> $TMP_DIR/cds.fa | cut -c2- | cut -d\  -f1) \
#                 <(grep \> $TMP_DIR/cds.fa | sed 's/.*\[protein_id=//' | cut -d] -f1)) \
#             >$TMP_DIR/gene2mrna2cds2ptn.csv
#     else
#         cp $GENE2PTNA $TMP_DIR/gene2mrna2cds2ptn.csv
#     fi

#     python3 <(printf "
#         from Bio import SeqIO
#         from Bio.SeqRecord import SeqRecord
#         import os
#         table = [l.strip().split(',') for l in open('$TMP_DIR/gene2mrna2cds2ptn.csv').readlines()[1:]]
#         gene2iso = [l.strip().split(',') for l in open('$TMP_DIR/to3d/transcript_gene_mapping.csv').readlines()[1:] if len(l)>3]
#         iso2gene = dict(gene2iso)
#         as_genes = set([l.strip() for l in open('$TMP_DIR/all_as_genes.txt').readlines() if len(l)>1])
#         as_iso = [x for x in gene2iso if x[1] in as_genes]
#         genes_as_iso = set([x[1] for x in as_iso])

#         print('GENES SEM CDS: ', ', '.join([x for x in as_genes if not x in genes_as_iso]))

#         cds = SeqIO.to_dict(SeqIO.parse('cds.fa', 'fasta'))
#         isos = [x[0] for x in as_iso]
#         isos_seq = [v for k, v in cds.items() if k in isos]
#         print('ISO SEM SEQ: ', ', '.join([x.id for x in isos_seq if not x.id in isos]))

#         ta_cds = isos_seq[0].id in [x[1] for x in table]
#         tdic = {(x[1] if ta_cds else x[2]): x[3] for x in table}

#         SeqIO.write([SeqRecord(c.seq.translate(), tdic[c.id], description=f'gene={iso2gene[c.id]}') for c in isos_seq], '$TMP_DIR/ptnas.faa', 'fasta')
#         open('$PTNAS', 'w').writelines([f'{x.id},{str(x.seq)}{os.linesep}' for x in SeqIO.parse('$TMP_DIR/ptnas.faa', 'fasta')])
#     " | cut -c9-) 1>$LOG_DIR/_6.4.1_ext_ptnas.log.txt 2>$LOG_DIR/_6.4.1_ext_ptnas.err.txt

#     [ -f $TMP_DIR/ptnas.faa ] && echo "Quantiade de proteins: $(grep -c \> $TMP_DIR/ptnas.faa)" >>$RESUMO
#     [ -f $TMP_DIR/ptnas.faa ] && echo "Tamanho total de proteins: $(grep -v \> $TMP_DIR/ptnas.faa | tr -d '\n' | wc -c)" >>$RESUMO

#     rm -f $TSV

#     if [ $ONLINE ]; then
#         [ ! -d $LOCAL ] && mkdir $LOCAL
#         local TT=$(grep -c , $PTNAS)

#         if (($(grep -c , $PTNAS) > 10)); then
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f1 | grep ,) 1 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f2 | grep ,) 2 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f3 | grep ,) 3 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f4 | grep ,) 4 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f5 | grep ,) 5 &

#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f6 | grep ,) 6 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f7 | grep ,) 7 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f8 | grep ,) 8 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f9 | grep ,) 9 &
#             anotar_api $LOCAL $Q $TSV $TT <(cat $PTNAS | paste - - - - - - - - - - | cut -f10 | grep ,) 0 &
#             wait
#             log 6 4 0 "anotou interpro ONLINE"
#         else
#             anotar_api $LOCAL $Q $TSV $TT $PTNAS 1
#         fi
#     else
#         if [ -f $LOCAL.tsv ]; then
#             log 6 4 0 "recuperoou interpro de $LOCAL.tsv"
#             cp $LOCAL.tsv $TSV
#         else
#             [ -f /tmp/interproscan.tar.gz ] && [ ! -f /tmp/interproscan*/interproscan.sh ] && cd /tmp && tar -xf /tmp/interproscan.tar.gz
#             cd $TMP_DIR
#             sed 's/[*.]$//' $PTNAS | grep -v '*' | awk '{print ">"$1}' | tr , \\n >ptns.faa
#             bash /tmp/interproscan*/interproscan.sh \
#                 -appl PANTHER,Pfam,SMART \
#                 -cpu 10 -f TSV -goterms -pa -verbose \
#                 -i ptns.faa -o $TSV 1>$LOG_DIR/_6.4.2_interproscan.log.txt 2>$LOG_DIR/_6.4.2_interproscan.err.txt
#             cp $TSV $LOCAL.tsv
#             log 6 4 0 "anotou interpro LOCAL"
#         fi
#     fi

#     echo "$(date +%d/%m\ %H:%M) terminou anotacao" >>$RESUMO
# }










else
    echo "skipping $L sucess run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) finished" >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"


