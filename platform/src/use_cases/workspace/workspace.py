from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.filter.filter import Filter
from use_cases.filter.filter_error import FilterError
from use_cases.workspace.data_source_configuration import DataSourceConfiguration

class Workspace:
    
    def __init__(self, id, visualizer_identifier=None, data_source_identifier=None, graph_data=None, path=None, graph_html=None, tree_view=None, data_source_configuration=None, filters=None):
        self.id = id
        self.path = path
        self.visualizer_identifier = visualizer_identifier
        self.data_source_identifier = data_source_identifier
        self.configuration = DataSourceConfiguration()
        if data_source_configuration:
            self.configuration.update(
                reference_attribute=data_source_configuration.get("reference_attribute"),
                is_graph_directed=data_source_configuration.get('is_graph_directed', True),
                loader_type=data_source_configuration.get("loader_type")
            )
        self.filters = filters or []
        self.graph_html = graph_html
        self.tree_view = tree_view
        self.graph_data = graph_data
        if graph_data:
            self.graph = Graph.from_dict(graph_data)
        else:
            self.graph = Graph()

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
        data_source.configure_plugin(
            reference_attribute = self.configuration.reference_attribute,
            loader = self.configuration.loader_type,
            is_graph_directed = self.configuration.is_graph_directed
        )
        if self.path and data_source:
            self.graph = data_source.load(path=self.path)
            self.graph_data = self.graph.to_dict()
        else:
            self.graph = Graph()


        self.graph_data = self.graph.to_dict()
        self.tree_view = tree_view_service.generate_template(self.graph)

    def show_graph(self, plugin_service, tree_view_service):
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)
        
        filtered_graph = self.get_filtered_graph()
        if visualizer:
            self.graph_html = visualizer.visualize(filtered_graph)
            self.graph_data = filtered_graph.to_dict()
        else:
            self.graph_html = "No visualizer selected 🚫"

        self.tree_view = tree_view_service.generate_template(filtered_graph)
        return self.graph_html

    def to_dict(self):
        return {
            "id": self.id,
            "visualizer_identifier": self.visualizer_identifier,
            "data_source_identifier": self.data_source_identifier,
            "path": self.path,
            "graph_data": self.graph.to_dict(),
            "data_source_configuration": self.configuration.to_dict(),
            "filters": [f.to_dict() if hasattr(f, "to_dict") else f for f in self.filters]
        }

    def refresh_visualization(self, plugin_service):
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)
        if visualizer:
            self.graph_html = visualizer.visualize(self.graph)
        else:
            self.graph_html = "No visualizer selected 🚫"

    @classmethod
    def from_dict(cls, data):
        filters = [Filter.from_dict(fd) for fd in data.get("filters", [])]
        return cls(
            id=data["id"],
            path=data.get("path"),
            data_source_identifier=data.get("data_source_identifier"),
            visualizer_identifier=data.get("visualizer_identifier"),
            filters=filters,
        )

    def add_filter(self, filters: Filter):
        try:
            self.graph.apply_filters(filters.to_dict())
            self.filters.append(filters)

        except FilterError as fe:
            raise fe

        return None

    def clear_filters(self):
        self.filters = []

    def get_filtered_graph(self) -> Graph:
        g = self.graph

        for f in self.filters:
            g = g.apply_filters(f.to_dict() if hasattr(f, "to_dict") else f)

        return g
