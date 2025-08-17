from dataclasses import dataclass, field

@dataclass
class Node:
    """
    Represents a single node (vertex) in a graph.

    Attributes:
        id (int): Unique identifier for the node.
        data (dict): Optional dictionary holding additional information about the node.
                     Defaults to an empty dictionary if not provided. Can store
                     arbitrary attributes like labels, names, or other metadata.
    """
    
    id: int
    data: dict = field(default_factory=dict)