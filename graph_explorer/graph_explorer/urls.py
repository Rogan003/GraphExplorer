from django.contrib import admin
from django.urls import path
from graph_explorer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
]
