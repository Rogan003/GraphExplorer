from abc import abstractmethod
from .base import Plugin
from api.graph_explorer_api.model.graph import Graph

class VisualizerPlugin(Plugin):
    """
    An abstraction representing a plugin for visualizing Graph objects.

    This class defines the interface that all visualizer plugins must implement.
    """

    @abstractmethod
    def visualize(self, graph: Graph, **kwargs) -> None:
        """
        Visualizes the given Graph object.

        :param graph: The Graph object to be visualized.
        :type graph: `Graph`
        :param kwargs: Arbitrary keyword arguments for customization of the visualization,
                       such as colors, layout options, labels, or rendering styles.
        :type kwargs: dict
        :return: None
        """
        pass