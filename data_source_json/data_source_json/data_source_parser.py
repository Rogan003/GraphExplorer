from __future__ import annotations
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_json.configuration import JSONLoaderType, JSONGraphType
from data_source_json.configuration import Configuration
from data_source_json.loader import JSONFileLoader, JSONLoader, JSONUrlLoader
from data_source_json.parser import JSONParser

class DataSourceJSONParser(DataSourcePlugin):
    loader: JSONLoader = JSONFileLoader()
    config: Configuration | None = Configuration()
    parser: JSONParser = JSONParser()

    def load(self, **kwargs) -> Graph:
        self.__configure_plugin()
        data = self.loader.load(kwargs.get("path"))
        reference_attribute = self.config.get_reference_attribute() if self.config else "reference"
        graph_type = self.config.get_graph_type() if self.config else "directed"
        return self.parser.parse(data, reference_attribute, graph_type)

    def __configure_plugin(self):
        loader_type = self.config.get_loader_type()
        if loader_type == JSONLoaderType.URL:
            self.loader = JSONUrlLoader()
        else:
            self.loader = JSONFileLoader()

    def identifier(self) -> str:
        return "DataSourceJSONParser"

    def name(self) -> str:
        return "Data source JSON parser"