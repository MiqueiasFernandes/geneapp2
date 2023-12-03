from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import GeneSerializer
from .models import Gene

@csrf_exempt
def genes(request):
    '''
    List all genes
    '''
    if(request.method == 'GET'):
        genes = Gene.objects.all()
        serializer = GeneSerializer(genes, many=True)
        return JsonResponse(serializer.data,safe=False)
    
    elif(request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = GeneSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def gene_detail(request, pk):
    try:
        # obtain the gene with the passed id.
        gene = Gene.objects.get(pk=pk)
    except:
        # respond with a 404 error message
        return HttpResponse(status=404)  
    if(request.method == 'PUT'):
        # parse the incoming information
        data = JSONParser().parse(request)  
        # instanciate with the serializer
        serializer = Gene(gene, data=data)
        # check whether the sent information is okay
        if(serializer.is_valid()):  
            # if okay, save it on the database
            serializer.save() 
            # provide a JSON response with the data that was submitted
            return JsonResponse(serializer.data, status=201)
        # provide a JSON response with the necessary error information
        return JsonResponse(serializer.errors, status=400)
    elif(request.method == 'DELETE'):
        # delete the gene
        gene.delete() 
        # return a no content response.
        return HttpResponse(status=204)
    return gene