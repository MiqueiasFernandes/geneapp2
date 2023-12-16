#!/bin/bash

if [ -d /rmats ]
then
    cd /rmats/rmats*turbo* 
    make || (cat <(head -2 Makefile ) <(tail -2 Makefile) > x && mv x Makefile && make)
else
    RMATS="https://github.com/Xinglab/rmats-turbo/releases/download/v4.1.2/rmats_turbo_v4_1_2.tar.gz"
    rm -rf /rmats && mkdir /rmats && cd /rmats
    echo baixando rMATS de $RMATS
    wget -O rmats $RMATS
    tar -xvf rmats 
    cd rmats_turbo* 
    make && cd .. && rm rmats && ln -s $(pwd)/$(ls rmats_turbo*/rmats.py) . && chmod +x rmats.py
fi
[ ! -f "/rmats/rmats.py" ] && echo "-> ❌ ERROR ON RMATS INSTALL !!!"
[ -f "/rmats/rmats.py" ] && echo "-> ✅ RMATS INSTALED !!!"


# cc -Wall -O2 -msse2 -funroll-loops -fopenmp -o rMATSexe src/main.c src/myfunc.c src/util.c 
# lbfgs_scipy/lbfgsb.o lbfgs_scipy/linpack.o lbfgs_scipy/timer.o -lm -lgfortran -lgsl 
# -lgslcblas -lgomp -lblas -llapack
# cc: error: unrecognized command-line option '-msse2'
