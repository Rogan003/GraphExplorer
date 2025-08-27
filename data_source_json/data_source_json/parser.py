import json

from datetime import datetime

from graph_explorer_api.model.edge import Edge
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.model.node import Node
from data_source_json.configuration import JSONGraphType

class JSONParser:
    __graph: Graph = Graph()
    __nodes: dict[str, Node] = {}  # node_id -> Node
    __edges_to_resolve: list[tuple[str, str]] = []  # (from_id, to_id)
    __reference_attribute: str = "reference"

    def parse(self, data: str, reference_attribute: str, graph_type: JSONGraphType) -> Graph:
        self.__reset()  # so different instances won't use the same values
        self.__reference_attribute = reference_attribute
        self.__graph.directed = graph_type == JSONGraphType.DIRECTED

        json_data = json.loads(data)
        self.__build_graph(json_data, parent_id=None)
        self.__resolve_edges()

        return self.__graph

    def __reset(self):
        self.__graph = Graph()
        self.__nodes = {}
        self.__edges_to_resolve = []

    def __build_graph(self, json_data, parent_id=None):
        if not isinstance(json_data, dict):
            return

        # if no @id => generate value
        root_node_id = json_data.get("@id") or str(len(self.__nodes))

        node_data = {}
        for key, val in json_data.items():
            if isinstance(val, (dict, list)):
                continue
            # collect node attributes
            if key not in ["@id", self.__reference_attribute]:
                node_data[key] = self.__convert_value(val)

        if root_node_id not in self.__nodes:
            node = Node(root_node_id, node_data)
            self.__nodes[root_node_id] = node
            self.__graph.nodes.append(node)
        else:
            self.__nodes[root_node_id].data.update(node_data)

        current_node = self.__nodes[root_node_id]

        # add `parent -> current` edge if it exists
        if parent_id and parent_id in self.__nodes:
            self.__add_edge(self.__nodes[parent_id], current_node)

        if self.__reference_attribute in json_data:
            self.__edges_to_resolve.append((str(root_node_id), str(json_data[self.__reference_attribute])))

        # go through children
        for _, val in json_data.items():
            if isinstance(val, dict):
                self.__build_graph(val, parent_id=root_node_id)
            elif isinstance(val, list):
                for item in val:
                    self.__build_graph(item, parent_id=root_node_id)

    """
    Add an edge depending on graph type (directed/undirected).
    """
    def __add_edge(self, from_node: Node, to_node: Node):
        if self.__graph.directed:
            if not self.__edge_exists(from_node, to_node):
                self.__graph.edges.append(Edge(from_node, to_node))
        else:
            if not self.__edge_exists(from_node, to_node):
                self.__graph.edges.append(Edge(from_node, to_node))
            if not self.__edge_exists(to_node, from_node):
                self.__graph.edges.append(Edge(to_node, from_node))

    def __edge_exists(self, a: Node, b: Node) -> bool:
        return any(e.from_node == a and e.to_node == b for e in self.__graph.edges)

    """
    Resolve parent/child edges after building the graph.
    """
    def __resolve_edges(self):
        for src_id, target_id in self.__edges_to_resolve:
            if src_id in self.__nodes and target_id in self.__nodes:
                self.__add_edge(self.__nodes[src_id], self.__nodes[target_id])

    def __convert_value(self, value):
        if isinstance(value, str):
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                pass
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass
            return value  # string
        return value
