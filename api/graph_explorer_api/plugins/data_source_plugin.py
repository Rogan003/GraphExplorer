from abc import abstractmethod

from graph_explorer_api.plugins.data_source_loaders import DataSourceLoader

from .base import Plugin
from graph_explorer_api.model.graph import Graph

class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading data from a specific data source.
    """
    reference_attribute: str
    loader: DataSourceLoader
    is_graph_directed: bool

    @abstractmethod
    def load(self, path: str) -> Graph:
        """
        Loads data from the data source and returns it as a `Graph` object.

        :param path: Path to the file or url to the web.
        :return: `Graph` object loaded from the data source.
        :rtype: Graph
        """
        pass

    def configure_plugin(self, reference_attribute: str, loader: DataSourceLoader, is_graph_directed: bool):
        self.reference_attribute = reference_attribute
        self.loader = loader
        self.is_graph_directed = is_graph_directed