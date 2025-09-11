import os
from graph_explorer_api.model.graph import Graph
from datetime import date, datetime
from jinja2 import FileSystemLoader, Environment
from graph_explorer_api.plugins.visualizer_plugin import VisualizerPlugin 

class SimpleVisualizerPlugin(VisualizerPlugin):

  def name(self) -> str:
    return "Simple Visualizer"
  
  def identifier(self) -> str:
    return "simple_visualizer"

  def safe_value(self, value):
      if isinstance(value, datetime):
          return value.strftime("%d.%m.%Y. %H:%M")  # "24.08.2025. 21:15" (date and time)
      elif isinstance(value, date):
          return value.strftime("%d.%m.%Y.")  # "24.08.2025." (only date)
      return str(value)

  def sanitize_data(self, data) -> dict:
      if not isinstance(data, dict):
          return {}
      return {k: self.safe_value(v) for k, v in data.items() if k is not None and v is not None}

  def visualize(self, graph: Graph, **kwargs) -> str:
    p = os.path.dirname(__file__)
    path = os.path.join(p, "templates")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template("simple_visualizer.html")

    nodes_js = [ 
      {"id": str(n.id),
       "data": self.sanitize_data(n.data)}
      for n in graph.nodes
    ]

    edges_js = [
      {
        "source": str(e.from_node.id),
        "target": str(e.to_node.id),
        "directed": graph.directed,
        "data": self.sanitize_data(e.data)
      }
      for e in graph.edges
    ]

    context = {
      "nodes": nodes_js,
      "edges": edges_js,
      "directed": graph.directed
    }

    return template.render(context)
