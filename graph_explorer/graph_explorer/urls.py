from django.urls import path
from graph_explorer import views

urlpatterns = [
    path('', views.index, name='index'), 
]