
#########   oque é o gene app  ######### 

                        |-> /api       Django geneappserver   disponibiliza os arquivos resultados
 usuario ----> nginx ---|-> /          Nuxt = geneappexplorer frontend
                        |-> /service   Flask = geneappscritp  executa as analises de integracao

#########   como montar em dev  ######### 

 -backend
   cd backend
   python3 -m venv django_env
   source django_env/bin/activate
   pip3 install -r requirements.txt --no-cache-dir
   cd geneapp
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py runserver 0.0.0.0:8000

 -frontend
   cd frontend/geneappexplorer
   npm ci && npm run dev

-service
   cd geneapp2
   docker compose down && docker compose build
   docker run -p 9000:9000 -v ./data:/tmp/geneappdata -v ./service:/app mikeiasfernandes93/geneapp2service

#########   como biudar para prd  #########  
  cd deploy_prd_dir
  git clone ....
  configurar variaveis
  cd geneapp2 && mkdir data/projects
  docker compose down && docker compose build && docker compose --env-file profile.env up -d && docker compose logs


######### deploy aws   #########
apt install htop git
git clone https://github.com/MiqueiasFernandes/geneapp2.git
cd geneapp2/ && mkdir -p data/projects
nano profile.env
sudo docker compose down && sudo docker compose build && sudo docker compose --env-file profile.env up -d && sudo docker compose logs

sudo rm -rf geneapp2/ && git clone https://github.com/MiqueiasFernandes/geneapp2.git && mv profile.env geneapp2/ && cd geneapp2/ && sudo docker compose down && sudo docker compose build && sudo docker compose --env-file profile.env up -d

#########   licenca  #########  
 - o geneapp e seus modulos sao de propriedade registrada da ufmg e ufv
 - somente é admitido uso em pesquisa sem fim comercial
 - o resultados devem ser validados pelo pesquisador
 - os softwares que o geneapp executa como rmats e 3dranseq tem licencas especificas que devem ser obervadas



#########   limitacoes  #########  
-filtrando gene single exon

mkdir /tmp/geneappdata/projects/2023-12-05_e3576547-0d65-4dbe-8f12-fbd7caab4312/inputs -p

 ### copiar
curl -d "projeto=projects/2023-12-05_e3576547-0d65-4dbe-8f12-fbd7caab4312" -X POST http://localhost:9000/copiar_arquivo/server.txt/servidor.txt

### baixar 
curl -d "projeto=projects/2023-12-05_e3576547-0d65-4dbe-8f12-fbd7caab4312" -d "arquivo=https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_rna.fna.gz" -X POST http://localhost:9000/baixar_arquivo/transcritos.fna

### descompactar
curl -d "projeto=projects/2023-12-05_e3576547-0d65-4dbe-8f12-fbd7caab4312" -X POST http://localhost:9000/descomprimir_arquivo/transcritos.fna.gz