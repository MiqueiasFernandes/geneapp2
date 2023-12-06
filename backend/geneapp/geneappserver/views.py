from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import ProjetoSerializer
from .models import  Projeto
from .geneappscript import *

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
            return JsonResponse(serializer.data, status=201), self.klass.objects.get(pk=id)
        return JsonResponse(serializer.errors, status=400), None
    
    def update(self, request, item):
        data = JSONParser().parse(request) 
        serializer = self.klass(item, data=data) 
        if(serializer.is_valid()):  
            serializer.save() 
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, item):
        item.delete()
        return HttpResponse(status=204)
    
    def handle(self, request, pk=None):
        if request.method == 'GET':
            if pk is None:
                return self.list(), None
        elif(request.method == 'POST'): 
            return self.create(request)

        try:
            item = self.klass.objects.get(pk=pk)
        except:
            return HttpResponse(status=404), None
        
        if request.method == 'GET':
            return JsonResponse(self.seralizer(item).data, safe=False), item
        elif request.method == 'PUT':
            return self.update(request, item), item
        elif request.method == 'DELETE':
            return self.delete(item), item

        return HttpResponse(status=400), None


crud_projetos = CRUD(Projeto, ProjetoSerializer)

@csrf_exempt
def projetos(request):
    response, obj = crud_projetos.handle(request)
    if obj:
        try:
            obj.path = str(criar_proj())
            obj.save()
            json = crud_projetos.seralizer(obj).data
            print(json)
            write_data(f"{obj.path}/geneapp.txt", str(json))
            return JsonResponse(json, safe=False)
        except:
            obj.delete()
            return HttpResponse(status=507)
    return response

def projeto(request, pk):
    response, obj = crud_projetos.handle(request, pk)
    return response

