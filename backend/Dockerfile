FROM python:bullseye
WORKDIR /backend 
COPY requirements.txt /backend
RUN pip3 install -r requirements.txt --no-cache-dir
COPY geneapp /backend 
ENTRYPOINT ["python3"]
RUN rm -f /backend/db.sqlite3
RUN /backend/manage.py makemigrations geneappserver && /backend/manage.py migrate
CMD ["/backend/manage.py", "runserver", "0.0.0.0:8000"]