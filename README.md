
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
   docker run -p 9000:9000 geneapp2-flask

#########   como buildar para prd  #########  
  cd deply_prd_dir
  git clone ....
  configurar variaveis
  cd geneapp2 && mkdir data/projects
  docker compose down && docker compose build && docker compose up -d && docker compose logs

#########   licenca  #########  
 - o geneapp e seus modulos sao de propriedade registrada da ufmg e ufv
 - somente é admitido uso em pesquisa sem fim comercial
 - o resultados devem ser validados pelo pesquisador
 - os softwares que o geneapp executa como rmats e 3dranseq tem licencas especificas que devem ser obervadas