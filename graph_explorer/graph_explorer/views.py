from django.shortcuts import render
from django.apps import apps
from use_cases.const import VISUALIZER_GROUP
from use_cases.const import DATA_SOURCE_GROUP

def index(request):
    plugin_service = apps.get_app_config('graph_explorer').plugin_service

    data_source_plugins = plugin_service.plugins[DATA_SOURCE_GROUP]
    selected_data_source_plugin = data_source_plugins[0] if data_source_plugins else None
    
    graph = selected_data_source_plugin.load(path="../data_source_xml/data_source_xml/test_files/test.xml")

    visualizer_plugins = plugin_service.plugins[VISUALIZER_GROUP]

    print("PLUGINS: " + str(visualizer_plugins))

    selected = visualizer_plugins[0] if visualizer_plugins else None
    graph_html = selected.visualize(graph) if selected else "No visualizer selected 🚫"

    return render(request, "index.html", {
        "plugins": visualizer_plugins,
        "graph_html": graph_html,
        "selected_plugin": selected.identifier() if selected else None
    })
