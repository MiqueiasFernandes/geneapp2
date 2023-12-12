
RESET=$1
DJANGO=./backend/geneapp/manage.py

[ $RESET ] && rm -rf data/projects/geneapp* backend/geneapp/geneappserver/migrations backend/geneapp/db.sqlite3
[ $RESET ] &&  docker compose down && docker compose build
source ./backend/django_env/bin/activate 
[ $RESET ] &&  $DJANGO makemigrations geneappserver  &&  $DJANGO migrate

docker run -p 9000:9000 -v ./data:/tmp/geneappdata geneapp2-flask &
$DJANGO runserver &
cd frontend/geneappexplorer/ && npm run dev &

wait