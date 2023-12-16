#!/bin/bash
source /geneapp_env/bin/activate
bh=$(pip show deeptools | grep "Location: " | cut -d\  -f2)/deeptools/bamHandler.py
if ! grep 'pysam.index(bamFile)' $bh 1>/dev/null 2>/dev/null; then
    echo "corrigindo o arquivo $bh ..."
    cp $bh .
    cp bamHandler.py $bh.old
    grep -B100000 'bam = pysam.Samfile(bamFile' bamHandler.py | grep -v 'bam = pysam.Samfile(bamFile' >xtemp
    echo '        pysam.index(bamFile)' >>xtemp
    tail bamHandler.py -n+$(grep -n 'bam = pysam.Samfile(bamFile' bamHandler.py | cut -d: -f1) >>xtemp
    cp xtemp $bh
    rm xtemp bamHandler.py
else
    echo "-> ✅ DeepTools FIXED !!!"
fi
