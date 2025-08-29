from django.urls import path
from graph_explorer import views

urlpatterns = [
    path('', views.index, name='index'), 
    path("cli/execute/", views.cli_execute, name="cli_execute"),
]