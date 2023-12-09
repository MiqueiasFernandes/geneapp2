from django.urls import path 
from geneappserver import views

# define the urls
urlpatterns = [

    path('project', views.project),
    path('project/<int:pk>', views.project),

    path('command', views.command),
    path('command/<int:pk>', views.command),

]