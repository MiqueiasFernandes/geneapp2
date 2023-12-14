from rest_framework import serializers
from .models import Project, Sample, Command

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['id', 'name', 'acession', 'local_path', 'group']

class CommandSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    project_id = serializers.IntegerField(required=False)

    class Meta:
        model = Command
        fields = ['id', 'project_id', 'op', 'status', 'success', 'end', 'log', 'err', 'out', 
                  'info', 'meta', 'created_at', 'started_at', 'ended_at', 'tsp', 'lock',
                  'arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9']

    def create(self, validated_data):
        prj = Project.objects.get(pk = validated_data.pop('project_id'))
        cmd = Command.objects.create(project=prj, **validated_data)
        cmd.save()
        return cmd

    def update(self, instance: Command, validated_data):

        if instance.project is None:
            ## so permite setar o prj once
            prj = Project.objects.get(pk=validated_data.pop('project_id'))
            instance.project = prj

        if (not instance.project is None) and (instance.status is None): 
            ## somente premite atualizar cmd para promover para executar
            instance.status = validated_data.get('status', instance.status)
        
        instance.info = validated_data.get('info', instance.info)
        instance.save()
        return instance

    
class ProjectSerializer(serializers.ModelSerializer):
    samples = SampleSerializer(many=True)
    commands = CommandSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Project
        fields = ['id',
            'name', 'control', 'treatment',
            'path', 'organism',  'created_at',  
            'online', 'fast', 'library','status',
            'genome', 'anotattion', 'proteome', 'transcriptome', 
            'threads', 'ram', 'disk', 'qvalue','psi', 'rmats_readLength',  
            'samples', 'commands'
            ]
        
    def create(self, validated_data):
        samples = validated_data.pop('samples')
        assert len(samples) < 20
        commands = validated_data.pop('commands')
        project = Project.objects.create(**validated_data)
        for sample in samples:
            Sample.objects.create(project=project, **sample)
        for command in commands:
            Command.objects.create(project=project, **command)
        return project
    
    def update(self, instance, validated_data):

        commands_data = validated_data.pop('commands')

        for command in commands_data:
            id = command.get('id')
            if id is None:
                obj = Command.objects.create(project=instance, **command)
            else:
                obj = Command.objects.get(pk=id)
                obj.project = instance if obj.project is None else obj.project
                obj.status = command.get('status') if (not obj.project is None) and (obj.status is None) else obj.status
                obj.info = command.get('info', obj.info)
            obj.save()
            
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
