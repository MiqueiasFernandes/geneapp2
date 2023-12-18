#!/bin/bash

# if [ -d /rmats ]
# then
#     cd /rmats/rmats*turbo* 
#     make || (cat <(head -2 Makefile ) <(tail -2 Makefile) > x && mv x Makefile && make)
# else
    # RMATS="https://github.com/Xinglab/rmats-turbo/releases/download/v4.1.2/rmats_turbo_v4_1_2.tar.gz"
    RMATS=https://github.com/Xinglab/rmats-turbo/releases/download/v4.2.0/rmats_turbo_v4_2_0.tar.gz
    rm -rf /rmats && mkdir /rmats && cd /rmats
    echo baixando rMATS de $RMATS
    wget -O rmats $RMATS
    tar -xvf rmats 
    cd rmats_turbo* 
    sed -i s/-msse2// rMATS_C/Makefile  && make && 
    cd .. && rm rmats && ln -s $(pwd)/$(ls rmats_turbo*/rmats.py) . && chmod +x rmats.py
# fi
[ ! -f "/rmats/rmats.py" ] && echo "-> ❌ ERROR ON RMATS INSTALL !!!" && exit 1
[ -f "/rmats/rmats.py" ] && echo "-> ✅ RMATS INSTALED !!!"


# cc -Wall -O2 -msse2 -funroll-loops -fopenmp -o rMATSexe src/main.c src/myfunc.c src/util.c 
# lbfgs_scipy/lbfgsb.o lbfgs_scipy/linpack.o lbfgs_scipy/timer.o -lm -lgfortran -lgsl 
# -lgslcblas -lgomp -lblas -llapack
# cc: error: unrecognized command-line option '-msse2'



# 1  wget
#     2  apt install wget
#     3  sudo 
#     4  apt update
#     5  apt install wget
#     6  wget https://github.com/Xinglab/rmats-turbo/releases/download/v4.2.0/rmats_turbo_v4_2_0.tar.gz
#     7  ls
#     8  mkdir rmats
#     9  cd rmats
#    10  ls
#    11  cp ../rmats_turbo_v4_2_0.tar.gz .
#    12  gunzip rmats_turbo_v4_2_0.tar.gz 
#    13  ls
#    14  tar -xvf rmats_turbo_v4_2_0.tar 
#    15  ls
#    16  cd rmats_turbo_v4_2_0
#    17  ls
#    18  make
#    19  apt install cmake
#    20  make
#    21  apt install g++
#    22  make
#    23  apt install zlib
#    24  apt install zlib1g-dev
#    25  make
#    26  apt install gfortran
#    27  make
#    28  ls ../
#    29  cp Makefile makeFile
#    30  make || (cat <(head -2 Makefile ) <(tail -2 Makefile) > x && mv x Makefile && make)
#    31  make
#    32  apt install python-is-python3
#    33  make
#    34  apt-get install python3-distutils
#    35  make
#    36  apt-get install python3-distutils cython3
#    37  make
#    38  ls
#    39  python rmats.py 
#    40  histry




