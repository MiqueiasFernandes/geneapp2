



# 7 quantificar com salmon
log 5 $SID 7 "quantificando com a amostra $SAMPLE com salmon"
if [ $IS_PE ]; then
    salmon quant -1 $TMP_SAMPLE/$SAMPLE.F.fq -2 $TMP_SAMPLE/$SAMPLE.R.fq -o $TMP_SAMPLE/quant_$SAMPLE --libType IU --index $TMP_DIR/idxcds \
        1>$LOG_DIR/_5.$SID.7_quant.$SAMPLE.log.txt 2>$LOG_DIR/_5.$SID.7_quant.$SAMPLE.err.txt
else
    salmon quant -r $TMP_SAMPLE/$SAMPLE.fq -o $TMP_SAMPLE/quant_$SAMPLE --libType IU --index $TMP_DIR/idxcds \
        1>$LOG_DIR/_5.$SID.7_quant.$SAMPLE.log.txt 2>$LOG_DIR/_5.$SID.7_quant.$SAMPLE.err.txt
fi
mkdir $QNT_DIR/sample_$SAMPLE && cp $TMP_SAMPLE/quant_$SAMPLE/quant.sf $QNT_DIR/sample_$SAMPLE/quant.sf
echo "$(date +%d/%m\ %H:%M) CDS expressa em $SAMPLE: $(cut -f4 $TMP_SAMPLE/quant_$SAMPLE/quant.sf | tail -n+2 | grep -cv '^0$')" >>$RESUMO
