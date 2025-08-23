from abc import abstractmethod
from .base import Plugin
from graph_explorer_api.model.graph import Graph

class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading data from a specific data source.
    """

    @abstractmethod
    def load(self, **kwargs) -> Graph:
        """
        Loads data from the data source and returns it as a `Graph` object.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: dict
        :return: `Graph` object loaded from the data source.
        :rtype: Graph
        """
        pass