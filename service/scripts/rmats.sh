#!/bin/bash
PROJECTS=$1 ## /tmp/geneappdata/projects
PROJ=$2     ## 2023-12-08_c7f88f0d-f4b6-40ec-9c0e-71da742579c3
ID=$3       ## 99
BAM1=$4   ## bam1,bam2
BAM2=$5    ## bam3,bam4
PARAM=$6    ## -t single
RLEN=$7    ## 150 reads leng

I=$PROJECTS/$PROJ/inputs
R=$PROJECTS/$PROJ/results
LOG=$PROJECTS/$PROJ/jobs/job.$ID.out.txt
ERR=$PROJECTS/$PROJ/jobs/job.$ID.err.txt
touch $LOG
touch $ERR
L=RMATS

echo ".... RMATS $RLEN ...." > $LOG 
echo BAM1 : $BAM1
echo BAM2 : $BAM2

echo S $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"
echo $PARAM
[ ! -d "$R/quants" ] && mkdir $R/quants

if ! grep -q "$L" $R/status.txt ; then
    mkdir $R/rmats
    echo $BAM1 > $I/bam1.txt
    echo $BAM2 > $I/bam2.txt
    /rmats/rmats.py \
        --b1 $I/bam1.txt --b2 $I/bam2.txt --gtf $R/genes.gtf \
        --od $I/rmats_out --tmp $I/rmats_tmp \
       $PARAM --readLength $RLEN  1>>$LOG 2>>$ERR &&
       cp $I/rmats_out/*JCEC.txt $I/rmats_out/summary.txt $R/rmats
else
    echo "skipping $L sucess rmats run"
    sleep 1
fi

echo "$L $(date +%d/%m\ %H:%M) sample mapped." >> $R/status.txt
echo TERMINADO_COM_SUCESSO
echo E $ID `date -Iseconds` >> "$PROJECTS/$PROJ/jobs/jobs.txt"





####### ######### ############ ######### ############ #############  ##############
####### ######### ############ ######### ############ #############  ##############
####### ######### ############ ######### ############ #############  ##############
####### ######### ############ ######### ############ #############  ##############
# /rmats/rmats.py --b1 bams1 --b2 bams2 --gtf genes.gtf -t single 
# --od $(pwd)/rmats_out --tmp $(pwd)/tmp_out --readLength 50

# python3 rmats/rmats.py --b1 $CTRL --b2 $CASE --gtf gene.gtf -t single \
#         --od rmats_out \
#         --tmp tmp_out \
#         $RMATS_ARG1 $RMATS_ARG2 $RMATS_ARG3 $RMATS_ARG4 \
#         1>$LOG_DIR/_6.1.1_rmats.log.txt 2>$LOG_DIR/_6.1.1_rmats.err.txt
#     ## --readLength 150 --variable-read-length --nthread 1



# make[2]: Entering directory '/data/rmats_turbo_v4_2_0/rMATS_C/lbfgs_scipy'
# f77 -c -O2  -c -o lbfgsb.o lbfgsb.f
# f77 -c -O2  -c -o linpack.o linpack.f
# f77 -c -O2  -c -o timer.o timer.f
# make[2]: Leaving directory '/data/rmats_turbo_v4_2_0/rMATS_C/lbfgs_scipy'
# cc -Wall -O2 -msse2 -funroll-loops -fopenmp -o rMATSexe src/main.c src/myfunc.c src/util.c lbfgs_scipy/lbfgsb.o lbfgs_scipy/linpack.o lbfgs_scipy/timer.o -lm -lgfortran -lgsl -lgslcblas -lgomp -lblas -llapack
# cc: error: unrecognized command-line option '-msse2'
# make[1]: *** [Makefile:40: rMATSexe] Error 1


# apt install wget cmake g++ zlib1g-dev gfortran python-is-python3 cython3 libblas-dev liblapack-dev
# sed -i s/-msse2// rMATS_C/Makefile && make


