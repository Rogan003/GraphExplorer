import os
from datetime import date, datetime

from jinja2 import FileSystemLoader, Environment
from graph_explorer_api.plugins.visualizer_plugin import VisualizerPlugin 
from graph_explorer_api.model.graph import Graph

class BlockVisualizerPlugin(VisualizerPlugin):
  
  def name(self) -> str:
    return "Block Visualizer"
  
  def identifier(self) -> str:
    return "block_visualizer"

  def safe_value(self, value):
      if isinstance(value, datetime):
          return value.strftime("%d.%m.%Y. %H:%M")  # "24.08.2025. 21:15" (date and time)
      elif isinstance(value, date):
          return value.strftime("%d.%m.%Y.")  # "24.08.2025." (only date)
      return str(value)

  def visualize(self, graph: Graph, **kwargs) -> str:
    p = os.path.dirname(__file__)
    path = os.path.join(p, "templates")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template('block_visualizer.html')

    nodes_js = [
        {
            "id": str(n.id),
            "name": str(n.data.get('name', n.id)) if n.data.get('name', n.id) is not None else str(n.id),
            "attributes": [
                {"name": key, "value": self.safe_value(value)}
                for key, value in n.data.items()
                if key is not None and value is not None and key != 'name'
            ],
            "data": n.data
        }
        for n in graph.nodes
    ]

    edges_js = [
        {
            "source": str(e.from_node.id),
            "target": str(e.to_node.id),
            "directed": graph.directed,
            "data": e.data
        }
        for e in graph.edges
    ]

    context = {
        "nodes": nodes_js,
        "edges": edges_js,
        "directed": graph.directed
    }

    return template.render(context)

