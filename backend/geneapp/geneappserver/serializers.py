from rest_framework import routers,serializers,viewsets
from .models import Projeto

class ProjetoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'name', 'path',  'created_at', 'organism']

