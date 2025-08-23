import json
from django.shortcuts import render
from django.apps import apps
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.model.edge import Edge
from graph_explorer_api.model.node import Node
from use_cases.const import VISUALIZER_GROUP

def index(request):

    # Temporary hardcoded data for testing until the data source plugin is implemented.
    
    n1 = Node(id="n1", data={"first": "John", "last": "Doe", "years": 50})
    n2 = Node(id="n2", data={"first": "Alice", "last": "Smith", "years": 30})
    n3 = Node(id="n3", data={"first": "Bob", "last": "Brown", "years": 40})
    n4 = Node(id="n4", data={"first": "Carol", "last": "White", "years": 25})

    e1 = Edge(from_node=n1, to_node=n2)
    e2 = Edge(from_node=n2, to_node=n3)
    e3 = Edge(from_node=n3, to_node=n4)
    e4 = Edge(from_node=n2, to_node=n4)

    graph = Graph(
        nodes=[n1, n2, n3, n4],
        edges=[e1, e2, e3, e4],
        directed=True
    )

    plugin_service = apps.get_app_config('graph_explorer').plugin_service
    visualizer_plugins = plugin_service.plugins[VISUALIZER_GROUP]

    print("PLUGINS: " + str(visualizer_plugins))

    selected = visualizer_plugins[0] if visualizer_plugins else None
    graph_html = selected.visualize(graph) if selected else "No visualizer selected 🚫"

    return render(request, "index.html", {
        "plugins": visualizer_plugins,
        "graph_html": graph_html,
        "selected_plugin": selected.identifier() if selected else None
    })
