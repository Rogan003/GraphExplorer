from graph_explorer_api.model.graph import Graph
from graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_xml.parser import XmlParser

class DataSourceXmlParser(DataSourcePlugin):
    parser: XmlParser = XmlParser()

    def load(self, path: str) -> Graph:
        xml = self.loader.load(path)
        if not xml or len(xml) == 0:
            return Graph()

        return self.parser.parse_xml(xml, self.reference_attribute, self.is_graph_directed)

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"