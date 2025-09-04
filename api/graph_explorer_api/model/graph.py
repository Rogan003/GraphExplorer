from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List
from use_cases.filter.filter_error import FilterError

from .node import Node
from .edge import Edge

@dataclass
class Graph:
    """
    Represents a graph structure consisting of nodes and edges.

    Attributes:
        nodes (List[Node]): List of nodes in the graph.
        edges (List[Edge]): List of edges in the graph.
        directed (bool): True if the graph is directed.
    """
    
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    directed: bool = False

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def remove_node(self, node_id: int):
        node = self.get_node(node_id)
        self.nodes.remove(node)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

    def has_edges(self, node_id: int) -> bool:
      return any(edge.from_node.id == node_id or edge.to_node.id == node_id for edge in self.edges)

    def edit_node(self, node: Node, properties: dict):
      for key, value in properties.items():
          node.data[key] = value  

      return node
  
    def get_node(self, node_id: int) -> Node:
      for node in self.nodes:
          if node.id == node_id:
              return node
      raise ValueError(f"Node with id {node_id} does not exist.")

    def to_dict(self):
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "directed": self.directed,
        }

    @classmethod
    def from_dict(cls, data):
        g = cls(directed=data.get("directed", False))
        g.nodes = [Node.from_dict(nd) for nd in data.get("nodes", [])]
        g.edges = [Edge.from_dict(ed) for ed in data.get("edges", [])]
        return g

    from datetime import date, datetime

    def __parse_date(self, value: str) -> date:
        """
        Try to parse the input string to datetime.date.
        Allowed formats:
        - YYYY-MM-DD (ISO standard)
        - DD.MM.YYYY
        """
        try:
            # ISO format
            return date.fromisoformat(value)
        except ValueError:
            pass

        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            pass

        raise ValueError(f"Invalid date format: {value}. Use YYYY-MM-DD or DD.MM.YYYY")

    def apply_filters(self, filters):
        attribute_name = filters["attribute_name"]
        comparator = filters["comparator"]
        attribute_value = filters["attribute_value"]
        search = filters["search_value"]

        filtered_nodes = []

        if (search == "") and (attribute_name == "" or comparator == "" or attribute_value == ""):
            return self

        for node in self.nodes:
            ok_filter = True
            ok_search = True

            if attribute_name and comparator and attribute_value:
                if attribute_name not in node.data:
                    ok_filter = False
                else:
                    node_value = node.data[attribute_name]
                    node_type = type(node_value)

                    try:
                        if node_type is int:
                            filter_val = int(attribute_value)
                        elif node_type is float:
                            filter_val = float(attribute_value)
                        elif node_type is str:
                            filter_val = str(attribute_value)
                        elif node_type is date:
                            filter_val = self.__parse_date(attribute_value)
                        else:
                            raise FilterError(f"Unsupported attribute type: {node_type.__name__}")
                    except Exception:
                        raise FilterError(
                            f"Cannot convert '{attribute_value}' to {node_type.__name__} for filtering"
                        )

                    if comparator == "==":
                        ok_filter = node_value == filter_val
                    elif comparator == "!=":
                        ok_filter = node_value != filter_val
                    elif comparator in (">", ">=", "<", "<="):
                        if isinstance(node_value, (int, float, date)):
                            if comparator == ">":
                                ok_filter = node_value > filter_val
                            elif comparator == ">=":
                                ok_filter = node_value >= filter_val
                            elif comparator == "<":
                                ok_filter = node_value < filter_val
                            elif comparator == "<=":
                                ok_filter = node_value <= filter_val
                        else:
                            raise FilterError(
                                f"Comparator '{comparator}' not supported for type {node_type.__name__}"
                            )
                    else:
                        raise FilterError(f"Unknown comparator: {comparator}")

            if search:
                ok_search = False
                s = search.lower()
                for k, v in node.data.items():
                    if s in str(k).lower() or s in str(v).lower():
                        ok_search = True
                        break

            if ok_filter and ok_search:
                filtered_nodes.append(node)

        filtered_node_ids = {n.id for n in filtered_nodes}
        filtered_edges = [
            e for e in self.edges if e.from_node.id in filtered_node_ids and e.to_node.id in filtered_node_ids
        ]

        return Graph(nodes=filtered_nodes, edges=filtered_edges, directed=self.directed)
