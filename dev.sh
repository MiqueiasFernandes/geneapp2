
RESET=$1
DJANGO=./backend/geneapp/manage.py

[ $RESET ] && rm -rf data/projects/geneapp* backend/geneapp/geneappserver/migrations backend/geneapp/db.sqlite3
[ $RESET ] &&  docker compose down
source ./backend/django_env/bin/activate 
[ $RESET ] &&  $DJANGO makemigrations geneappserver  &&  $DJANGO migrate

cd frontend/geneappexplorer && npm ci && npm run build && cd ../../

$DJANGO runserver &
cd frontend/geneappexplorer/ && npm run dev && ../../ &
docker run -p 9000:9000 -v ./data:/tmp/geneappdata -v ./service:/app mikeiasfernandes93/geneapp2service
