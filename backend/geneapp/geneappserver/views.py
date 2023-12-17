from django.shortcuts import render
##import yaml
# Create your views here.

from rest_framework.parsers import JSONParser
from rest_framework_yaml.parsers import YAMLParser
from io import BytesIO
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
from .cmd_handler.CMD10Index import CMD10Index
from .cmd_handler.CMD11QCSample import CMD11QCSample
from .cmd_handler.CMD12Mapping import CMD12Mapping
from .cmd_handler.CMD13Quantify import CMD13Quantify


handlers = [CMD01Show(), CMD02Copy(), CMD03Download(), CMD04Unzip(), 
            CMD05Qinput(), CMD06Splitx(), CMD07Joinx(), CMD08Holder(), CMD09Qinput2(),
            CMD10Index(), CMD11QCSample(), CMD12Mapping(), CMD13Quantify()]

class CRUD:
    def __init__(self, klass, serializer) -> None:
        self.klass = klass
        self.seralizer = serializer

    def list(self):
        items = self.klass.objects.all()
        serializer = self.seralizer(items, many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def create(self, request, yaml=None):
        serializer=yaml
        if serializer is None:
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
def create_project(request):
    if request.method == 'POST':
        try:
            ## curl -F "yaml=@Downloads/geneapp.yaml" -X POST localhost:8000/api/create_project

            file_yaml = request.FILES['yaml']
            charset = "utf8" if file_yaml.charset is None else file_yaml.charset
            raw = "".join([line.decode(charset) for line in file_yaml]).replace("\n\n", "\n")

            data = YAMLParser().parse(BytesIO(bytearray(raw, "utf8")), parser_context={"encoding": "utf8"})

            # {'Project': {'Name': 'Project Fungi', 'Organism': 'Candida albicans'}, 
            #  'Input Files': {'remote': True, 'Genome': 'https:/fna.gz', 'Anotattion': 'httCF/nomic.gff.gz', 
            #                  'Transcriptome': 'httpfna.gz', 'Proteome': 'https:2/9SM18296v3_protein.faa.gz'}, 
            # 'Contrast group': {'Library layout': 'SHORT_SINGLE', 
            #                    'Control': {'label': 'WILD', 
            #                                'samples': [{'acession': 'SRR2513862'}, {'acession': 'SRR2513864'}]}, 
            #                     'Treatment': {'label': 'TREATED', 
            #                                 'samples': [{'acession': 'SRR2513867'}, 'SRR2513869'}]}}, 
            # 'Params configuration': {'Fast mode': False, 'PSI': 0.1, 'Qvalue': 0.05, 'rMATS read lengt': 50}}

            prj = data["Project"]
            inputs = data["Input Files"]
            contrast = data["Contrast group"]
            configs = data["Params configuration"]

            def parse_samples(dsamples):
                smps = []
                cont = 1
                for smp in dsamples["samples"]:
                    acession = smp["acession"]
                    group = dsamples["label"]
                    name = f"{group.lower()}{cont}.fq"
                    smps.append({"acession": acession, "group": group, "name": name})
                    cont += 1
                return smps

            dx = {
                    # id = IntegerField(required=False)
                    "name" : prj["Name"], 
                    "organism" : prj["Organism"],
                    "control" : contrast["Control"]["label"],
                    "treatment" : contrast["Treatment"]["label"], 
                    # path = CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
                    # created_at = DateTimeField(read_only=True)
                    "online":  not inputs['remote'] is None and inputs['remote'] != "No",
                    # fast = BooleanField(required=False)
                    "library": contrast['Library layout'],
                    # status = IntegerField(required=False)
                    "genome" : inputs["Genome"],
                    "anotattion" : inputs["Anotattion"],
                    "proteome" : inputs["Proteome"],
                    "transcriptome" : inputs["Transcriptome"],
                    # threads = IntegerField(max_value=100, min_value=1, required=False)
                    # ram = IntegerField(max_value=100, min_value=1, required=False)
                    # disk = IntegerField(max_value=100, min_value=1, required=False)
                    "qvalue": configs["Qvalue"],
                    "psi": configs["PSI"],
                    "rmats_readLength": configs["rMATS read lengt"],
                    "samples" : parse_samples(contrast["Control"]) + parse_samples(contrast["Treatment"]),
                    #     id = IntegerField(label='ID', read_only=True)
                    #     name = CharField(max_length=50)
                    #     acession = CharField(max_length=100)
                    #     local_path = CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
                    #     group = CharField(max_length=20)
                    "commands" :[{ ##= CommandSerializer(many=True):
                    #     id = IntegerField(required=False)
                    #     project_id = IntegerField(required=False)
                        "op" : 1,
                        "status" : "exec",
                    #     success = BooleanField(required=False)
                    #     end = BooleanField(required=False)
                    #     log = CharField(allow_blank=True, allow_null=True, max_length=999, required=False)
                    #     err = CharField(allow_blank=True, allow_null=True, max_length=999, required=False)
                    #     out = CharField(allow_blank=True, allow_null=True, max_length=999, required=False)
                    #     info = CharField(allow_blank=True, allow_null=True, max_length=999, required=False)
                    #     meta = CharField(allow_blank=True, allow_null=True, max_length=999, required=False)
                    #     created_at = DateTimeField(read_only=True)
                    #     started_at = CharField(allow_blank=True, allow_null=True, max_length=50, required=False)
                    #     ended_at = CharField(allow_blank=True, allow_null=True, max_length=50, required=False)
                    #     tsp = IntegerField(max_value=999999, required=False)
                    #     lock = IntegerField(max_value=999999, required=False)
                        "payload" : raw,
                        "arg1" :"geneapp.yaml"
                    #     arg2 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg3 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg4 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg5 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg6 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg7 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg8 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                    #     arg9 = CharField(allow_blank=True, allow_null=True, max_length=200, required=False)
                        }]
                }
            
            serializer = ProjectSerializer(data=dx)
            _, obj = crud_projetos.create(None, yaml=serializer)

            print(_, obj)
            return project(request, pk = None, obj = obj)
        except:
            pass
    return HttpResponse(status=400)
    
@csrf_exempt ## ENDPOINT EXTERNAL OPEN
def project(request, pk = None, obj = None):

    if obj is None:
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

            assert not obj.path is None

            for command in obj.commands:
                try:
                    a, b = process(command)
                    if a:
                        b.save()
                except:
                    print("ERROR JOB", command)

            json = crud_projetos.seralizer(obj).data

            if pk is None: ## POST
                write_data(obj.path, "geneapp.json", str(json))

            return JsonResponse(json, safe=False)
        except:
            obj.delete()
            if obj.path: rm_proj(obj.path)
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
