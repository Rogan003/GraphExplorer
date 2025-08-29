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

    def to_dict(self):
        return {
            "from_node": self.from_node.to_dict(),
            "to_node": self.to_node.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            from_node=Node.from_dict(data["from_node"]),
            to_node=Node.from_dict(data["to_node"])
        )
