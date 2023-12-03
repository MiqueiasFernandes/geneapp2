from django.urls import path 
from geneappserver import views

# define the urls
urlpatterns = [

    path('projetos', views.projetos),
    path('projetos/<int:pk>', views.projeto),

    path('genes/', views.genes),
    path('genes/<int:pk>/', views.gene_detail),
]