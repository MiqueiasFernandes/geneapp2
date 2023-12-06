from django.urls import path 
from geneappserver import views

# define the urls
urlpatterns = [

    path('project', views.projects),
    path('project/', views.projects),
    path('project/<int:pk>', views.project),

    # path('samples', views.sample),
    # path('samples/', views.sample),
    # path('samples/<int:pk>', views.sample),

]