from django.urls import path 
from geneappserver import views

# define the urls
urlpatterns = [
    path('genes/', views.genes),
    path('genes/<int:pk>/', views.gene_detail),
]