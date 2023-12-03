from rest_framework import routers,serializers,viewsets
from .models import Gene
class GeneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'name', 'strand',  'created_at']