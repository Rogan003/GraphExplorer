from graph_explorer_api.model.graph import Graph
from graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_xml.loader import XmlLoader, XmlFileLoader, XmlLinkLoader
from data_source_xml.configuration import Configuration, XMLLoaderType
from data_source_xml.parser import XmlParser

class DataSourceXmlParser(DataSourcePlugin):
    loader: XmlLoader = XmlFileLoader()
    config: Configuration | None = Configuration()
    parser: XmlParser = XmlParser()

    def load(self, **kwargs) -> Graph:
        self.__configure_plugin()
        xml = self.loader.load(kwargs.get("path"))
        reference_attribute = self.config.get_reference_attribute() if self.config else "reference"
        return self.parser.parse_xml(xml, reference_attribute)

    def __configure_plugin(self):
        loader_type = self.config.get_loader_type()
        if loader_type == XMLLoaderType.LINK:
            self.loader = XmlLinkLoader()
        else:
            self.loader = XmlFileLoader()

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"