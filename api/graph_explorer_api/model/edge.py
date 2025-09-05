from __future__ import annotations

from dataclasses import dataclass, field
from .node import Node
from datetime import datetime, date

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
        def serialize(v):
            if isinstance(v, (datetime, date)):
                return v.isoformat()
            return v

        return {
            "id": self.id,
            "from_node": self.from_node.to_dict(),
            "to_node": self.to_node.to_dict(),
            "data": {k: serialize(v) for k, v in self.data.items()},
        }

    @classmethod
    def from_dict(cls, data):
        parsed_data = {}
        for k, v in data.get("data", {}).items():
            if isinstance(v, str):
                parsed_data[k] = cls.__parse_date(v)
            else:
                parsed_data[k] = v

        return cls(
            id=data["id"],
            from_node=Node.from_dict(data["from_node"]),
            to_node=Node.from_dict(data["to_node"]),
            data=parsed_data,
        )

    @staticmethod
    def __parse_date(value: str) -> date:
        """
        Try to parse the input string to datetime.date.
        Allowed formats:
        - YYYY-MM-DD (ISO standard)
        - DD.MM.YYYY
        """
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            pass
        raise ValueError(f"Invalid date format: {value}. Use YYYY-MM-DD or DD.MM.YYYY")