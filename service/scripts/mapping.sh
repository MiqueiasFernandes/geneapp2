

local SID=$1
local ETAPA=$2
local INDEX=$3
local SAMPLE=$4
local LABEL=$5
local IS_PE=$6

log 5 $SID $ETAPA "mapeando $SAMPLE no $LABEL com hisat2"
if [ $IS_PE ]; then
    hisat2 -x $INDEX -1 $SAMPLE.F.fq -2 $SAMPLE.R.fq --no-unal -S $SAMPLE.maped.sam \
        1>$LOG_DIR/_5.$SID.$ETAPA.map.$LABEL.$SAMPLE.log.txt 2>$LOG_DIR/_5.$SID.$ETAPA.map.$LABEL.$SAMPLE.err.txt
else
    hisat2 -x $INDEX -U $SAMPLE.fq --no-unal -S $SAMPLE.maped.sam \
        1>$LOG_DIR/_5.$SID.$ETAPA.map.$LABEL.$SAMPLE.log.txt 2>$LOG_DIR/_5.$SID.$ETAPA.map.$LABEL.$SAMPLE.err.txt
fi

# 4 mapear no genoma
[ $SKIP_MAP_GENOMA ] || mapear $SID 4 $TMP_DIR/idxgenoma $SAMPLE "GENOMA" $IS_PE
[ $SKIP_MAP_GENOMA ] && log 5 $SID 4 "pulando mapemento no genoma para amostra $SAMPLE"
if [ -f $SAMPLE.maped.sam ]; then
    log 5 $SID 4 "gerando bam de $SAMPLE para rMATS"
    samtools view -S -b $SAMPLE.maped.sam >$SAMPLE.maped.bam 2>$LOG_DIR/_5.$SID.4_bam.$SAMPLE.err.txt
    bamtools sort -in $SAMPLE.maped.bam -out $SAMPLE.rmats.bam 1>$LOG_DIR/_5.$SID.4_bamSort.$SAMPLE.log.txt 2>>$LOG_DIR/_5.$SID.4_bamSort.$SAMPLE.err.txt
    rm -rf $SAMPLE.maped.sam $SAMPLE.maped.bam
fi