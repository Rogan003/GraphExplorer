from lxml import etree, html

from graph_explorer_api.model.edge import Edge
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.model.node import Node

class XmlParser:
    __node_count: int = 0
    __references: [tuple[Node, str]] = []
    __xml_elements_to_graph_nodes: dict[etree._Element, Node] = {}
    __reference_attribute: str = "reference"
    __graph: Graph = Graph()
    __root_xml_element: etree._Element = None

    def parse_xml(self, xml: str, refrence_attribute: str, is_directed: bool) -> Graph:
        self.__graph.directed = is_directed
        self.__reference_attribute = refrence_attribute

        self.__root_xml_element = self.__parse_xml_root(xml)
        if self.__root_xml_element is None:
            return self. __graph

        self.__add_xml_tree_to_graph(self.__root_xml_element)

        self.__resolve_references()

        ret_graph = self.__graph
        self.__reset()
        return ret_graph

    def __parse_xml_root(self, xml: str) -> etree._Element:
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.fromstring(xml.encode("utf-8"), parser=parser)
        except Exception:
            return html.fromstring(xml)

    """
    Does a DFS over the XML tree and adds nodes and edges to the graph.
    Also saves all the references to create special referencing edges later.
    """
    def __add_xml_tree_to_graph(
            self,
            xml_node: etree._Element
    ) -> Node | tuple[str, str] | str | None:
        if len(xml_node.getchildren()) == 0:
            reference_value = xml_node.get(self.__reference_attribute)
            if reference_value is not None:
                return reference_value
            else:
                return xml_node.tag, xml_node.text

        data = {
            "name": xml_node.tag,
            "text": xml_node.text
        }
        if xml_node.attrib:
            data.update(xml_node.attrib)

        new_node = Node(self.__node_count, data)
        self.__node_count += 1
        self.__graph.nodes.append(new_node)
        self.__xml_elements_to_graph_nodes[xml_node] = new_node

        for child in xml_node.getchildren():
            child_node = self.__add_xml_tree_to_graph(child)

            if isinstance(child_node, Node):
                self.__graph.edges.append(Edge(new_node, child_node))

            # this means that child_node is a reference to another node
            elif isinstance(child_node, str):
                self.__references += [(new_node, child_node)]
                self.__node_count -= 1
                self.__graph.nodes.remove(new_node)
                self.__xml_elements_to_graph_nodes.pop(xml_node)
                return None

            # this means that child_node is a leaf node, here it becomes an attribute
            elif child_node is not None:
                data[child_node[0]] = child_node[1]

            # this only happens if the child node had a reference child, meaning it should be an edge
            else:
                self.__references[-1] = (new_node, self.__references[-1][1])

        return new_node

    def __resolve_references(self) -> Graph:
        # TODO: performance could be improved, think about doing that
        for node, reference in self.__references:
            for node_in_graph in self.__graph.nodes:
                if node_in_graph.id == node.id:
                    reference_node = self.__find_reference_node(reference)
                    if reference_node is None:
                        continue
                    self.__graph.edges.append(Edge(node, reference_node))
                    break

    def __find_reference_node(self, reference: str) -> Node | None:
        ref_node = self.__root_xml_element.xpath(reference)
        if len(ref_node) != 1:
            return None

        ref_node = ref_node[0]

        return self.__xml_elements_to_graph_nodes[ref_node]

    def __reset(self):
        self.__id = 0
        self.__references = []
        self.__xml_elements_to_graph_nodes = {}
        self.__graph = Graph()
        self.__node_count = 0