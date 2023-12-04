from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import ProjetoSerializer
from .models import  Projeto

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
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    def update(self, request, item):
        data = JSONParser().parse(request) 
        serializer = self.klas(item, data=data) 
        if(serializer.is_valid()):  
            serializer.save() 
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, item):
        item.delete()
        return HttpResponse(status=204)
    
    def handle(self, request, pk=None):
        if(request.method == 'GET'):
            return self.list()
        elif(request.method == 'POST'): 
            return self.create(request)
        
        try:
            item = self.klas.objects.get(pk=pk)
        except:
            return HttpResponse(status=404)
        
        if(request.method == 'PUT'):
            return self.update(request, item)
        elif(request.method == 'DELETE'):
            return self.delete(item)

        return HttpResponse(status=400)


crud_projetos = CRUD(Projeto, ProjetoSerializer)

@csrf_exempt
def projetos(request):
    return crud_projetos.handle(request)

def projeto(request, pk):
    return crud_projetos.handle(request, pk)

