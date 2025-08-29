from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
# import pdb

# TODO: add documentation

class Workspace:
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