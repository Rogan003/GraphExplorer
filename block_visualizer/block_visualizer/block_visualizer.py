import os
from jinja2 import FileSystemLoader, Environment
from graph_explorer_api.plugins.visualizer_plugin import VisualizerPlugin 
from graph_explorer_api.model.graph import Graph

class BlockVisualizerPlugin(VisualizerPlugin):
  
  def name(self) -> str:
    return "Block Visualizer"
  
  def identifier(self) -> str:
    return "block_visualizer"

  def visualize(self, graph: Graph, **kwargs) -> str:
    p = os.path.dirname(__file__)
    path = os.path.join(p, "templates")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template('block_visualizer.html')

    nodes_js = [
        {
            "id": str(n.id),
            "name": f"{n.data.get('first','')} {n.data.get('last','')}",
            "attributes": [
                {"name": "first", "value": n.data.get("first", "")},
                {"name": "last", "value": n.data.get("last", "")},
                {"name": "years", "value": n.data.get("years", "")}
            ]
        }
        for n in graph.nodes
    ]

    edges_js = [
        {
            "source": str(e.from_node.id),
            "target": str(e.to_node.id),
            "directed": graph.directed
        }
        for e in graph.edges
    ]

    context = {
        "nodes": nodes_js,
        "edges": edges_js,
        "directed": graph.directed
    }

    return template.render(context)

