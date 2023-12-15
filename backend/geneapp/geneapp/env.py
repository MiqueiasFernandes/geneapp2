import os


__DEV_SECRET_KEY = 'django-insecure-wq_0+15vb19*k81nw7cl618onr134z-r@2jc0ix+gks9b!bd-m' 
ENV_SECRET_KEY = os.getenv('DJANGO_KEY', __DEV_SECRET_KEY)

ENV_HOST = os.getenv('DJANGO_HOST', 'localhost')

ENV_PROF = os.getenv('DJANGO_PROF', 'DEV')
ENV_PROF_PRD = ENV_PROF == 'PRD'
ENV_PROF_DEV = not ENV_PROF_PRD

__debug = os.getenv('DJANGO_DEBUG', "UNSET")
ENV_DEBUG = (__debug == "UNSET" and ENV_PROF_DEV) or (__debug == "YES")

ENV_GENEAPP_SERVICE_API =  os.getenv('DJANGO_SERVICE_API', 'http://localhost:9000')

ENV_DATA_DIR = os.getenv('DJANGO_DATA', '/Users/miqueias/Local/geneapp2/data')
ENV_PROJECTS = f"{ENV_DATA_DIR}/projects"

ENV_DJANGO_RUNNING = os.getenv('DJANGO_SETTINGS_MODULE', "!") != "!"