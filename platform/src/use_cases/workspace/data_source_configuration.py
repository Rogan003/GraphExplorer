from dataclasses import dataclass
from enum import Enum
from graph_explorer_api.plugins.data_source_loaders import DataSourceLoader, DataSourceFileLoader
from use_cases.loader_service import find_loader


class GraphType(Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"

@dataclass
class DataSourceConfiguration:
    reference_attribute: str = "reference"
    graph_type: GraphType = GraphType.DIRECTED
    loader_type: DataSourceLoader = DataSourceFileLoader()

    def to_dict(self) -> dict:
        return {
            "reference_attribute": self.reference_attribute,
            "graph_type": self.graph_type.value,
            "loader_type": self.loader_type.identifier()
        }

    def update(self, reference_attribute: str, graph_type: str, loader_type: str):
       self.reference_attribute=reference_attribute
       self.graph_type=GraphType(
           graph_type
       )
       self.loader_type=find_loader(loader_type)