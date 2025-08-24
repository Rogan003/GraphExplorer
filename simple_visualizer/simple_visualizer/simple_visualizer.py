import os
from graph_explorer_api.model.graph import Graph
from jinja2 import FileSystemLoader, Environment
from graph_explorer_api.plugins.visualizer_plugin import VisualizerPlugin 

class SimpleVisualizerPlugin(VisualizerPlugin):

  def name(self) -> str:
    return "Simple Visualizer"
  
  def identifier(self) -> str:
    return "simple_visualizer"

  def visualize(self, graph: Graph, **kwargs) -> str:
    p = os.path.dirname(__file__)
    path = os.path.join(p, "templates")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template("simple_visualizer.html")

    nodes_js = [ 
      {"id": str(n.id)}
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
