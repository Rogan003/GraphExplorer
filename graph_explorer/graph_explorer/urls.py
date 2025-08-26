from django.urls import path
from graph_explorer import views

urlpatterns = [
    path('', views.index, name='index'),
    path("workspace/<int:workspace_id>/apply_filter/", views.apply_filter, name="apply_filter"),
    path("workspace/<int:workspace_id>/reset_filters/", views.reset_filters, name="reset_filters"),
]