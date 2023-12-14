from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import ProjectSerializer, SampleSerializer, CommandSerializer
from .models import  Project, Sample, Command
from .geneappscript import *

from .cmd_handler.CMD01Show import CMD01Show
from .cmd_handler.CMD02Copy import CMD02Copy
from .cmd_handler.CMD03Download import CMD03Download
from .cmd_handler.CMD04Unzip import CMD04Unzip
from .cmd_handler.CMD05Qinput import CMD05Qinput
from .cmd_handler.CMD06Splitx import CMD06Splitx
from .cmd_handler.CMD07Joinx import CMD07Joinx
from .cmd_handler.CMD08Holder import CMD08Holder
from .cmd_handler.CMD09Qinput2 import CMD09Qinput2

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
     
        if pk is None: ## POST
            obj.path = str(criar_proj())
            obj.save()

        if obj.path:
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
        else:
            obj.delete()
            if obj.path: rm_proj(obj.path)
            return HttpResponse(status=507)

    return response



crud_samples = CRUD(Sample, SampleSerializer)

@csrf_exempt ## ENDPOINT EXTERNAL OPEN
def sample(request, pk = None):
    response, _ = crud_samples.handle(request, pk)
    return response

handlers = [CMD01Show(), CMD02Copy(), CMD03Download(), CMD04Unzip(), 
            CMD05Qinput(), CMD06Splitx(), CMD07Joinx(), CMD08Holder(), CMD09Qinput2()]

crud_commands = CRUD(Command, CommandSerializer)

def process(command: Command):
    
    ## draft ou terminou
    if command.project is None or command.end:
        return False, command
    
    
    ## comando criado
    if command.status == 'exec':
        command.status = f'Nsubmetido'
       
        handled = False
        for handler in handlers:
            handled = handler.handle(command)
            if handled:
                break

        if not handled:
            command.status = "Finished"
            command.end = True
            command.err = "Error when submit job to service. No has handler."
            command.success = False

    elif not command.status is None: ## comando criado sem pedir para exec
        try:
            job = job_status(command.id)
            command.status = job['status']
            command.end = job['end']
            command.success = job['success']
            command.started_at, command.ended_at = get_time(command.project.path, command.id)
            if command.end:
                command.log, command.out, command.err = get_logs(command.project.path, command.id) 
        except:
            if command.status == 'skipped':
                command.err = f"Job skipped because dependence job tsp({command.lock}) raised error"
            else:
                command.err = 'Unknown error'
            command.status = 'unknown'
            command.end = True
            command.success = False
   
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
