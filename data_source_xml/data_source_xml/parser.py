from lxml import etree

from api.graph_explorer_api.model.edge import Edge
from api.graph_explorer_api.model.graph import Graph
from api.graph_explorer_api.model.node import Node
from api.graph_explorer_api.plugins.data_source_plugin import DataSourcePlugin
from data_source_xml.data_source_xml.loader import XmlLoader, XmlFileLoader, XmlLinkLoader
from data_source_xml.data_source_xml.configuration import Configuration, XMLLoaderType


class DataSourceXmlParser(DataSourcePlugin):
    id: int = 0
    loader: XmlLoader = XmlFileLoader()
    references: [tuple[Node, str]] = []
    xml_elements_to_graph_nodes: dict[etree._Element, Node] = {}
    config: Configuration | None = None

    def load(self, **kwargs) -> Graph:
        # Initialize configuration and select loader accordingly
        self.config = Configuration()
        loader_type = self.config.get_loader_type()
        if loader_type == XMLLoaderType.LINK:
            self._select_loader(XmlLinkLoader())
            source = kwargs.get("link")
            xml = self.loader.load(link=source)
        else:
            # Default to FILE
            self._select_loader(XmlFileLoader())  # now controlled by configuration
            file_path = kwargs.get("file_path", "../test_files/test.xml")
            xml = self.loader.load(file_path=file_path)

        # Reset state for each load call
        self.id = 0
        self.references = []
        self.xml_elements_to_graph_nodes = {}

        parsed_xml = self._parse_xml(xml)
        return parsed_xml

    def _select_loader(self, loader: XmlLoader):
        self.loader = loader

    def _parse_xml(self, xml: str) -> Graph:
        graph = Graph()
        graph.directed = True

        root_xml_element = self._parse_xml_root(xml)
        if root_xml_element is None:
            return graph

        self._dfs_recursive(root_xml_element, graph)

        self._resolve_references(root_xml_element, graph)

        return graph

    def _parse_xml_root(self, xml: str) -> etree._Element:
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.fromstring(xml.encode("utf-8"), parser=parser)

    def _dfs_recursive(self, node: etree._Element, graph: Graph) -> Node | tuple[str, str] | str | None:
        # Determine which attribute indicates a reference from configuration
        reference_attr = self.config.get_reference_attribute() if self.config else "reference"
        if len(node.getchildren()) == 0:
            if node.get(reference_attr) is not None:
                return node.get(reference_attr)
            else:
                return node.tag, node.text

        data = {
            "tag": node.tag,
            "text": node.text
        }
        for attribute in node.attrib:
            data[attribute] = node.attrib[attribute]

        new_node = Node(self.id, data)
        self.id += 1
        graph.nodes.append(new_node)
        self.xml_elements_to_graph_nodes[node] = new_node

        for child in node.getchildren():
            child_node = self._dfs_recursive(child, graph)

            if isinstance(child_node, Node):
                graph.edges.append(Edge(new_node, child_node))

            elif isinstance(child_node, str):
                self.references += [(new_node, child_node)]
                self.id -= 1
                graph.nodes.remove(new_node)
                self.xml_elements_to_graph_nodes.pop(node)
                return None

            elif child_node is not None:
                data[child_node[0]] = child_node[1]

            else:
                self.references[-1] = (new_node, self.references[-1][1])

        return new_node

    def _resolve_references(self, root_element: etree._Element, graph: Graph) -> Graph:
        # performance could be improved
        for node, reference in self.references:
            for node_in_graph in graph.nodes:
                if node_in_graph.id == node.id:
                    reference_node = self._find_reference_node(root_element, reference, graph)
                    if reference_node is None:
                        continue
                    graph.edges.append(Edge(node, reference_node))
                    break

    def _find_reference_node(self, root_element: etree._Element, reference: str, graph: Graph) -> Node | None:
        ref_node = root_element.xpath(reference)
        if len(ref_node) != 1:
            return None

        ref_node = ref_node[0]

        return self.xml_elements_to_graph_nodes[ref_node]

    def identifier(self) -> str:
        return "DataSourceXmlParser"

    def name(self) -> str:
        return "Data source xml parser"