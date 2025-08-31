from __future__ import annotations
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_json.parser import JSONParser

class DataSourceJSONParser(DataSourcePlugin):
    parser: JSONParser = JSONParser()

    def load(self, path: str) -> Graph:
        json = self.loader.load(path)

        if not json or len(json) == 0:
            return Graph()

        return self.parser.parse(json, self.reference_attribute, self.is_graph_directed)

    def identifier(self) -> str:
        return "DataSourceJSONParser"

    def name(self) -> str:
        return "Data source JSON parser"