from dataclasses import dataclass, field
from .node import Node

@dataclass
class Edge:
    """
    Represents an edge (connection) between two nodes in a graph.

    Attributes:
        id (int): Unique identifier for the edge.
        from_node (Node): The starting node of the edge.
        to_node (Node): The ending node of the edge.
        data (dict): Optional dictionary holding additional attributes about the edge.
                     Defaults to an empty dictionary if not provided. Can store
                     arbitrary attributes like labels, names, or other metadata.
    """
    id: int
    from_node: Node
    to_node: Node
    data: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "from_node": self.from_node.to_dict(),
            "to_node": self.to_node.to_dict(),
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            from_node=Node.from_dict(data["from_node"]),
            to_node=Node.from_dict(data["to_node"]),
            data=data.get("data", {})
        )