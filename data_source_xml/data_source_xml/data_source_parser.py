from graph_explorer_api.model.graph import Graph
from graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from graph_explorer_api.plugins.data_source_loaders import DataSourceUrlLoader, DataSourceFileLoader, DataSourceLoader
from data_source_xml.configuration import Configuration, XMLLoaderType, GraphType
from data_source_xml.parser import XmlParser

class DataSourceXmlParser(DataSourcePlugin):
    loader: DataSourceLoader = DataSourceFileLoader()
    config: Configuration | None = Configuration()
    parser: XmlParser = XmlParser()

    def load(self, **kwargs) -> Graph:
        self.__configure_plugin()
        xml = self.loader.load(kwargs.get("path"))
        reference_attribute = self.config.get_reference_attribute() if self.config else "reference"
        is_directed = self.config.get_graph_type() == GraphType.DIRECTED if self.config else True
        return self.parser.parse_xml(xml, reference_attribute, is_directed)

    def __configure_plugin(self):
        loader_type = self.config.get_loader_type()
        if loader_type == XMLLoaderType.LINK:
            self.loader = DataSourceUrlLoader()
        else:
            self.loader = DataSourceFileLoader()

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"