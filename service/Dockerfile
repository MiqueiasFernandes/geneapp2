FROM debian:bookworm

WORKDIR /app
COPY req*.txt geneappservice.sh geneappscript.py /app/
COPY scripts /app/scripts

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y task-spooler wget curl zip unzip 
RUN apt install -y sra-toolkit gffread
RUN apt install -y python3-pip python3-venv

RUN python3 -m venv /geneapp_env
RUN . /geneapp_env/bin/activate && pip install -r req_env_geneapp.txt --no-cache-dir

RUN python3 -m venv /flask_env
RUN . /flask_env/bin/activate && pip install -r requirements.txt --no-cache-dir

RUN chmod +x /app/scripts/*.sh /app/scripts/*py /app/geneappservice.sh

RUN groupadd geneappgp && useradd -g geneappgp geneappusr
USER geneappusr

ENTRYPOINT [ "/app/geneappservice.sh" , "flask", "run"]