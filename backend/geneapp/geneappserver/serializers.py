from rest_framework import routers,serializers,viewsets
from .models import Gene
from .models import Projeto

class ProjetoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'nome', 'path',  'created_at']

from .models import Gene
class GeneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'name', 'strand',  'created_at']