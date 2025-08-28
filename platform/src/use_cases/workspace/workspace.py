from graph_explorer_api.model.graph import Graph
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.filter.filter import Filter

class Workspace:
    def __init__(self, id, file_path=None, data_source_identifier=None, visualizer_identifier=None, filters=None):
        self.id = id
        self.file_path = file_path
        self.data_source_identifier = data_source_identifier
        self.visualizer_identifier = visualizer_identifier
        self.filters = filters or []

    def load_graph(self, plugin_service, tree_view_service):
        data_source = plugin_service.get_selected_plugin(DATA_SOURCE_GROUP, self.data_source_identifier)
        visualizer = plugin_service.get_selected_plugin(VISUALIZER_GROUP, self.visualizer_identifier)

        if self.file_path and data_source:
            self.graph = data_source.load(path=self.file_path)
        else:
            self.graph = Graph()

        filtered_graph = self.get_filtered_graph()

        if visualizer:
            self.graph_html = visualizer.visualize(filtered_graph)
        else:
            self.graph_html = "No visualizer selected 🚫"

        self.tree_view = tree_view_service.generate_template(filtered_graph)

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "data_source_identifier": self.data_source_identifier,
            "visualizer_identifier": self.visualizer_identifier,
            "filters": [f.to_dict() if hasattr(f, "to_dict") else f for f in self.filters],
        }

    @classmethod
    def from_dict(cls, data):
        filters = [Filter.from_dict(fd) for fd in data.get("filters", [])]
        return cls(
            id=data["id"],
            file_path=data.get("file_path"),
            data_source_identifier=data.get("data_source_identifier"),
            visualizer_identifier=data.get("visualizer_identifier"),
            filters=filters,
        )

    def add_filter(self, filters: Filter):
        self.filters.append(filters)

    def clear_filters(self):
        self.filters = []

    def get_filtered_graph(self) -> Graph:
        g = self.graph

        for f in self.filters:
            g = g.apply_filters(f.to_dict() if hasattr(f, "to_dict") else f)

        return g