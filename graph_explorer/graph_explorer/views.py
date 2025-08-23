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

        # Get full system path to the saved file
        file_path = fs.path(filename)

    visualizer_identifier = request.GET.get("visualizer")
    data_source_identifier = request.GET.get("datasource")

    plugin_service = apps.get_app_config('graph_explorer').plugin_service

    data_source_plugins = plugin_service.plugins[DATA_SOURCE_GROUP]
    selected_data_source_plugin = data_source_plugins[0] if data_source_plugins else None
    if data_source_identifier:
        for plugin in data_source_plugins:
            if plugin.identifier() == data_source_identifier:
                selected_data_source_plugin = plugin
                break
    
    graph = selected_data_source_plugin.load(path=file_path) if file_path else Graph()

    visualizer_plugins = plugin_service.plugins[VISUALIZER_GROUP]

    print("PLUGINS: " + str(visualizer_plugins))

    selected = visualizer_plugins[0] if visualizer_plugins else None
    if visualizer_identifier:
        for plugin in visualizer_plugins:
            if plugin.identifier() == visualizer_identifier:
                selected = plugin
                break

    graph_html = selected.visualize(graph) if selected else "No visualizer selected 🚫"

    return render(request, "index.html", {
        "visualizer_plugins": visualizer_plugins,
        "data_source_plugins": data_source_plugins,
        "graph_html": graph_html,
        "selected_visualizer_plugin": selected.identifier() if selected else None,
        "selected_data_source_plugin": selected_data_source_plugin.identifier() if selected_data_source_plugin else None
    })
