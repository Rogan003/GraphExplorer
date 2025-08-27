from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.workspace.data_source_configuration import DataSourceConfiguration

class Workspace:
    def __init__(self, id, path=None, data_source_identifier=None, visualizer_identifier=None, data_source_configuration=None):
        self.id = id
        self.path = path
        self.data_source_identifier = data_source_identifier
        self.visualizer_identifier = visualizer_identifier
        self.configuration = DataSourceConfiguration()
        if data_source_configuration:
            self.configuration.update(
                reference_attribute=data_source_configuration.get("reference_attribute"),
                is_graph_directed=data_source_configuration.get('is_graph_directed', True),
                loader_type=data_source_configuration.get("loader_type")
            )

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
        data_source.configure_plugin(
            reference_attribute = self.configuration.reference_attribute,
            loader = self.configuration.loader_type,
            is_graph_directed = self.configuration.is_graph_directed
        )
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)

        if self.path and data_source:
            self.graph = data_source.load(path=self.path)
        else:
            self.graph = Graph()

        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
        else:
            self.graph_html = "No visualizer selected 🚫"

        self.tree_view = tree_view_service.generate_template(self.graph)

    
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "data_source_identifier": self.data_source_identifier,
            "visualizer_identifier": self.visualizer_identifier,
            "data_source_configuration": self.configuration.to_dict()
        }