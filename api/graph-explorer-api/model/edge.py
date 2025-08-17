from dataclasses import dataclass
from .node import Node

@dataclass
class Edge:
    """
    Represents an edge (connection) between two nodes in a graph.

    Attributes:
        from_node (Node): The starting node of the edge.
        to_node (Node): The ending node of the edge.
    """
    
    from_node: Node
    to_node: Node
