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
