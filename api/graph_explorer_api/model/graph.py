from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
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

    def __post_init__(self):
        node_ids = {node.id for node in self.nodes}

        for edge in self.edges:
            if edge.from_node.id not in node_ids or edge.to_node.id not in node_ids:
                raise ValueError(f"Edge {edge} connects nodes not in the graph!")

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def remove_node(self, node: Node):
        self.nodes.remove(node)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

    def apply_filters(self, filters):
        attribute_name = filters["attribute_name"]
        comparator = filters["comparator"]
        attribute_value = filters["attribute_value"]
        search = filters["search"]

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
                    value = node.data[attribute_name]
                    try:
                        if comparator == "==":
                            ok_filter = str(value) == str(attribute_value)
                        elif comparator == "!=":
                            ok_filter = str(value) != str(attribute_value)
                        elif comparator == ">":
                            ok_filter = float(value) > float(attribute_value)
                        elif comparator == ">=":
                            ok_filter = float(value) >= float(attribute_value)
                        elif comparator == "<":
                            ok_filter = float(value) < float(attribute_value)
                        elif comparator == "<=":
                            ok_filter = float(value) <= float(attribute_value)
                        else:
                            raise ValueError(f"Nepoznat komparator: {comparator}")
                    except (ValueError, TypeError):
                        raise ValueError("Neodgovarajući tip vrednosti za filter")

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
