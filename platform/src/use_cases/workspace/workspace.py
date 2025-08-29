from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP

class Workspace:
    def __init__(self, id, file_path=None, data_source_identifier=None, visualizer_identifier=None, graph_html=None, tree_view=None):
        self.id = id
        self.file_path = file_path
        self.data_source_identifier = data_source_identifier
        self.visualizer_identifier = visualizer_identifier
        self.graph_html = graph_html
        self.tree_view = tree_view

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)

        if self.file_path and data_source:
            self.graph = data_source.load(path=self.file_path)
        else:
            self.graph = Graph()

        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
        else:
            self.graph_html = "No visualizer selected 🚫"

        self.tree_view = tree_view_service.generate_template(self.graph)

        return self.graph_html

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "data_source_identifier": self.data_source_identifier,
            "visualizer_identifier": self.visualizer_identifier,
            "graph_html": getattr(self, "graph_html", None),
            "tree_view": getattr(self, "tree_view", None),
        }
    
    def refresh_visualization(self, plugin_service):
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)
        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
        else:
            self.graph_html = "No visualizer selected 🚫"