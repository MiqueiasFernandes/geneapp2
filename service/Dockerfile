## rmats require --platform=linux/amd64 & bellow deps
FROM --platform=linux/amd64 debian:bookworm AS rmats

COPY scripts /app/scripts
RUN chmod +x /app/scripts/*.sh
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y wget python3-pip python3-venv
RUN apt install -y cmake gfortran libblas-dev liblapack-dev libgsl-dev cython3 python-is-python3
RUN bash /app/scripts/_install_rMATS.sh

FROM debian:bookworm
COPY --from=rmats /rmats /rmats
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y task-spooler wget curl zip unzip python3-pip python3-venv

COPY scripts /app/scripts
COPY req_env_geneapp.txt requirements.txt geneappservice.sh geneappscript.py /app/
RUN chmod +x /app/scripts/*.sh /app/scripts/*py /app/geneappservice.sh

## end rMATS intall
RUN apt update -y && apt install -y wget python3-pip python3-venv
RUN apt install -y cmake gfortran libblas-dev liblapack-dev libgsl-dev cython3 python-is-python3
RUN bash /app/scripts/_install_rMATS.sh

## t3drnaseq require deps
RUN apt install -y r-base libxml2-dev libssl-dev libcurl4-openssl-dev libgsl-dev 
RUN apt install -y libfontconfig1-dev libgit2-dev libharfbuzz-dev libfribidi-dev
RUN apt install -y libpng-dev libtiff5-dev libjpeg-dev libfreetype6-dev

## geneapp deps
RUN apt install -y sra-toolkit gffread fastqc salmon samtools bamtools hisat2 trimmomatic 

## flask pyenv
RUN python3 -m venv /flask_env
RUN . /flask_env/bin/activate && pip install -r /app/requirements.txt --no-cache-dir

## geneapp pyenv
RUN python3 -m venv /geneapp_env
RUN . /geneapp_env/bin/activate && pip install -r /app/req_env_geneapp.txt --no-cache-dir

RUN bash /app/scripts/_fix_deeptools.sh
RUN Rscript scripts/_install_R_deps.R

RUN groupadd geneappgp && useradd -g geneappgp geneappusr
#USER geneappusr

ENTRYPOINT [ "/app/geneappservice.sh" , "flask", "run"]
