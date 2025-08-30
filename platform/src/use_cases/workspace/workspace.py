from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP

class Workspace:
    """
    Represents a workspace containing a graph, its visualization, and associated metadata.

    Attributes:
        id (int | str): Unique identifier for the workspace.
        visualizer_identifier (str, optional): Identifier of the selected visualizer plugin.
        data_source_identifier (str, optional): Identifier of the selected data source plugin.
        graph_data (dict, optional): Serialized representation of the graph.
        file_path (str, optional): Path to the file from which the graph is loaded.
        graph_html (str, optional): HTML representation of the graph visualization.
        tree_view (any, optional): Tree view template generated from the graph.
        graph (Graph): The actual Graph object associated with this workspace.

    Methods:
        load_graph(plugin_service, tree_view_service):
            Loads the graph from the selected data source or creates an empty graph if none exists.
            Updates `graph_data` and `tree_view` accordingly.

        show_graph(plugin_service, tree_view_service) -> str:
            Generates and returns the HTML visualization of the graph using the selected visualizer.
            Updates `graph_data` and `tree_view`.

        to_dict() -> dict:
            Returns a dictionary representation of the workspace, including serialized graph data.

        refresh_visualization(plugin_service):
            Refreshes the graph HTML visualization using the currently selected visualizer.
    """
    
    def __init__(self, id, visualizer_identifier=None, data_source_identifier=None, graph_data=None, file_path=None, graph_html=None, tree_view=None):
        self.id = id
        self.file_path = file_path
        self.visualizer_identifier = visualizer_identifier
        self.data_source_identifier = data_source_identifier
        self.graph_html = graph_html
        self.tree_view = tree_view
        self.graph_data = graph_data
        if graph_data:
            self.graph = Graph.from_dict(graph_data)
        else:
            self.graph = Graph()

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
        if self.file_path and data_source:
            self.graph = data_source.load(path=self.file_path)
            self.graph_data = self.graph.to_dict()
        else:
            self.graph = Graph()

        self.graph_data = self.graph.to_dict()
        self.tree_view = tree_view_service.generate_template(self.graph)

    def show_graph(self, plugin_service, tree_view_service):
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)
        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
            self.graph_data = self.graph.to_dict()
        else:
            self.graph_html = "No visualizer selected 🚫"

        self.tree_view = tree_view_service.generate_template(self.graph)
        return self.graph_html

    def to_dict(self):
        return {
            "id": self.id,
            "visualizer_identifier": self.visualizer_identifier,
            "data_source_identifier": self.data_source_identifier,
            "file_path": self.file_path,
            "graph_data": self.graph.to_dict()
        }

    def refresh_visualization(self, plugin_service):
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)
        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
        else:
            self.graph_html = "No visualizer selected 🚫"