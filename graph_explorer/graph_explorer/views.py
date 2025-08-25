from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.apps import apps

from use_cases.const import VISUALIZER_GROUP
from use_cases.const import DATA_SOURCE_GROUP
from graph_explorer_api.model.graph import Graph

def index(request):
    file_path = None
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        file_path = fs.path(filename)

    plugin_service = apps.get_app_config('graph_explorer').plugin_service
    visualizer_identifier = request.GET.get("visualizer")
    data_source_identifier = request.GET.get("datasource")

    data_source_plugins = plugin_service.plugins[DATA_SOURCE_GROUP]
    selected_data_source_plugin = plugin_service.get_selected_plugin(group=DATA_SOURCE_GROUP, identifier=data_source_identifier)

    visualizer_plugins = plugin_service.plugins[VISUALIZER_GROUP]
    selected_visualizer_plugin = plugin_service.get_selected_plugin(group=VISUALIZER_GROUP, identifier=visualizer_identifier)

    graph = selected_data_source_plugin.load(path=file_path) if file_path else Graph()
    graph_html = selected_visualizer_plugin.visualize(graph) if selected_visualizer_plugin else "No visualizer selected 🚫"

    tree_view_service = apps.get_app_config('graph_explorer').tree_view_service
    tree_view = tree_view_service.generate_template(graph)

    return render(request, "index.html", {
        "visualizer_plugins": visualizer_plugins,
        "data_source_plugins": data_source_plugins,
        "graph_html": graph_html,
        "selected_visualizer_plugin": selected_visualizer_plugin.identifier() if selected_visualizer_plugin else None,
        "selected_data_source_plugin": selected_data_source_plugin.identifier() if selected_data_source_plugin else None,
        "tree_view": tree_view
    })
