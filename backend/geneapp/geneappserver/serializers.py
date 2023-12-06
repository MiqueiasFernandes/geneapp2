from rest_framework import routers,serializers,viewsets
from .models import Project, Sample

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['name', 'acession', 'local_path', 'group']


class ProjectSerializer(serializers.ModelSerializer):
    samples = SampleSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id',
            'name', 'control', 'treatment',  'samples',
            'path', 'organism',  'created_at',  
            'online', 'fast', 'library','status',
            'genome', 'anotattion', 'proteome', 'transcriptome', 
            'threads', 'ram', 'disk', 'qvalue','psi'
            ]
        
    def create(self, validated_data):
        samples = validated_data.pop('samples')
        project = Project.objects.create(**validated_data)
        for sample in samples:
            Sample.objects.create(project=project, **sample)
        return project

