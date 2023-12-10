from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import ProjectSerializer, SampleSerializer, CommandSerializer
from .models import  Project, Sample, Command
from .geneappscript import *
from datetime import datetime

class CRUD:
    def __init__(self, klass, serializer) -> None:
        self.klass = klass
        self.seralizer = serializer

    def list(self):
        items = self.klass.objects.all()
        serializer = self.seralizer(items, many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def create(self, request):
        data = JSONParser().parse(request)
        serializer = self.seralizer(data=data)
        if(serializer.is_valid()):
            id= serializer.save().id
            obj = self.klass.objects.get(pk=id)
            return JsonResponse(self.seralizer(obj).data, status=201), obj
        return JsonResponse(serializer.errors, status=400), None
    
    def update(self, request, item):
        data = JSONParser().parse(request) 
        serializer = self.seralizer(item, data=data)
        if(serializer.is_valid()):  
            id = serializer.save().id
            obj = self.klass.objects.get(pk=id)
            return JsonResponse(serializer.data, status=201), obj
        return JsonResponse(serializer.errors, status=400)

    def delete(self, item):
        item.delete()
        return HttpResponse(status=204)
    
    def handle(self, request, pk=None):
        if request.method == 'GET':
            if pk is None:
                return self.list(), None
        elif(request.method == 'POST'): 
            return self.create(request) ## , None

        try:
            item = self.klass.objects.get(pk=pk)
        except:
            return HttpResponse(status=404), None
        
        if request.method == 'GET':
            return JsonResponse(self.seralizer(item).data), item
        elif request.method == 'PUT':
            return self.update(request, item) ## , item
        elif request.method == 'DELETE':
            return self.delete(item), item

        return HttpResponse(status=400), None


crud_projetos = CRUD(Project, ProjectSerializer)

@csrf_exempt ## ENDPOINT EXTERNAL OPEN
def project(request, pk = None):
    response, obj = crud_projetos.handle(request, pk)
    if obj:
        if request.method == 'DELETE':
            if not rm_proj(obj.path):
                print("ERROR RM PRJ", obj)
            return response
        try:
            if pk is None: ## POST
                obj.path = str(criar_proj())
                obj.save()

            for command in obj.commands:
                try:
                    a, b = process(command)
                    if a:
                        b.save()
                except:
                    print("ERROR JOB", command)

            json = crud_projetos.seralizer(obj).data

            if pk is None: ## POST
                write_data(obj.path, "geneapp.txt", str(json))

            return JsonResponse(json, safe=False)
        except:
            obj.delete()
            rm_proj(obj.path)
            return HttpResponse(status=507)

    return response



crud_samples = CRUD(Sample, SampleSerializer)

@csrf_exempt ## ENDPOINT EXTERNAL OPEN
def sample(request, pk = None):
    response, _ = crud_samples.handle(request, pk)
    return response


crud_commands = CRUD(Command, CommandSerializer)

def process(command: Command):

    ## draft ou terminou
    if command.project is None or command.end:
        return False, command
    
    ## comando criado
    if command.status == 'exec':
        command.status = f'Nsubmetido'
        error = False
        if command.op == 1:
            if job_show(command.project.path, command.id, command.arg1, command.arg2):
                command.status = 'submetido'
            else:
                error = True

        elif command.op == 2:
            if job_copiar(command.project.path, command.id, command.arg1, command.arg2):
                command.status = 'submetido'
            else:
                error = True

        elif command.op == 3:
            if job_baixar(command.project.path, command.id, 
                          command.arg1, command.arg2, command.arg3, command.project.library == "SHORT_PAIRED"):
                command.status = 'submetido'
            else:
                error = True

        elif command.op == 4:
            if job_unzip(command.project.path, command.id, command.arg1):
                command.status = 'submetido'
            else:
                error = True

        elif command.op == 5:
            if job_qinput(command.project.path, command.id, command.arg1, command.arg2, command.arg3, command.arg4):
                command.status = 'submetido'
            else:
                error = True

        else:
            command.status = f'errorOP[{command.op}]'

        if error:
            command.status = "Finished"
            command.end = True
            command.err = "Error when submit job to service"
            command.success = False

    elif not command.status is None:
        try:
            job = job_status(command.id)
            command.status = job['status']
            command.end = job['end']
            command.success = job['success']
            if command.end:
                command.log, command.out, command.err = get_logs(command.project.path, command.id) 
        except:
            command.status = 'unknown'
            command.err = 'Unknown error'
            command.end = True
            command.success = False
    
    if command.end:
        command.ended_at = datetime.now()
    return True, command


@csrf_exempt ## ENDPOINT EXTERNAL OPEN
def command(request, pk = None):
    response, obj = crud_commands.handle(request, pk)
    if not obj is None:
        alterou, command = process(obj)
        if alterou:
            command.save()
            json = crud_commands.seralizer(command).data
            return JsonResponse(json, status=201)
        
    return response
