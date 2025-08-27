from django.urls import path
from graph_explorer import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data_source_config', views.data_source_config, name='data_source_config')
]