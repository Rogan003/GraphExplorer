from dataclasses import dataclass
from graph_explorer_api.plugins.data_source_loaders import DataSourceLoader, DataSourceFileLoader
from use_cases.loader_service import find_loader

@dataclass
class DataSourceConfiguration:
    reference_attribute: str = "reference"
    is_graph_directed: bool = True
    loader_type: DataSourceLoader = DataSourceFileLoader()

    def to_dict(self) -> dict:
        return {
            "reference_attribute": self.reference_attribute,
            "is_graph_directed": self.is_graph_directed,
            "loader_type": self.loader_type.identifier()
        }

    def update(self, reference_attribute: str, is_graph_directed: bool, loader_type: str):
        self.reference_attribute=reference_attribute
        self.is_graph_directed=is_graph_directed
        self.loader_type=find_loader(loader_type)