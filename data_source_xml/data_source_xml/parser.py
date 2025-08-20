from api.graph_explorer_api.model.graph import Graph
from api.graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_xml.data_source_xml.loader import DataSourceXmlLoader, DataSourceXmlFileLoader


class DataSourceXmlParser(DataSourcePlugin):
    loader: DataSourceXmlLoader = DataSourceXmlFileLoader("path.xml")

    def load(self, **kwargs) -> Graph:
        self._select_loader(DataSourceXmlFileLoader("path.xml")) # make it not hard-coded through configuration
        xml = self.loader.load(**kwargs)
        _parse_xml = self._parse_xml(xml)
        return _parse_xml

    def _parse_xml(self, xml: str) -> Graph:
        pass

    def _select_loader(self, loader: DataSourceXmlLoader):
        self.loader = loader

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"