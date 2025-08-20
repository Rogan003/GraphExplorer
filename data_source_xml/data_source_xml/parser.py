from lxml import etree

from api.graph_explorer_api.model.edge import Edge
from api.graph_explorer_api.model.graph import Graph
from api.graph_explorer_api.model.node import Node
from api.graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_xml.data_source_xml.loader import XmlLoader, XmlFileLoader


class DataSourceXmlParser(DataSourcePlugin):
    id: int = 0
    loader: XmlLoader = XmlFileLoader()

    def load(self, **kwargs) -> Graph:
        self._select_loader(XmlFileLoader()) # make it not hard-coded through configuration

        xml = self.loader.load("../test_files/test.xml")

        parsed_xml = self._parse_xml(xml)
        return parsed_xml

    def _select_loader(self, loader: XmlLoader):
        self.loader = loader

    def _parse_xml(self, xml: str) -> Graph:
        graph = Graph()
        graph.directed = True

        root_xml_element = self.parse_xml_root(xml)
        if root_xml_element is None:
            return graph

        self.dfs_recursive(root_xml_element, graph)

        return graph

    def parse_xml_root(self, xml: str) -> etree._Element:
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.fromstring(xml.encode("utf-8"), parser=parser)

    def dfs_recursive(self, node: etree._Element, graph: Graph) -> Node | tuple[str, str]:
        if len(node.getchildren()) == 0:
            return node.tag, node.text

        data = {
            "tag": node.tag,
            "text": node.text
        }
        new_node = Node(self.id, data)
        self.id += 1
        graph.nodes.append(new_node)

        for child in node.getchildren():
            child_node = self.dfs_recursive(child, graph)

            if isinstance(child_node, Node):
                graph.edges.append(Edge(new_node, child_node))

            else:
                data[child_node[0]] = child_node[1]

        return new_node

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"