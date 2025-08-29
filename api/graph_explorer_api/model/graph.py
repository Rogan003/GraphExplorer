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

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def remove_node(self, node: Node):
        self.nodes.remove(node)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

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
