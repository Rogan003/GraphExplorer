from dataclasses import dataclass, field
from datetime import date, datetime

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

    def to_dict(self):
        def serialize(v):
            if isinstance(v, (datetime, date)):
                return v.isoformat()
            return v

        return {
            "id": self.id,
            "data": {k: serialize(v) for k, v in self.data.items()},
        }

    @classmethod
    def from_dict(cls, data):
        parsed_data = {}
        for k, v in data.get("data", {}).items():
            if isinstance(v, str):
                try:
                    parsed_data[k] = cls.__parse_date(v)
                except ValueError:
                    parsed_data[k] = v  # keep as string if not valid date
            else:
                parsed_data[k] = v

        return cls(
            id=data["id"],
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