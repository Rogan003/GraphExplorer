from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.workspace.data_source_configuration import DataSourceConfiguration, GraphType

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
                graph_type=data_source_configuration.get('graph_type', GraphType.DIRECTED.value),
                loader_type=data_source_configuration.get("loader_type")
            )

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
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