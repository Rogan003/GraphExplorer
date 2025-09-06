from __future__ import annotations

import json

from datetime import datetime

from graph_explorer_api.model.edge import Edge
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.model.node import Node

class JSONParser:
    __graph: Graph = Graph()
    __nodes: dict[int, Node] = {}  # node_id -> Node
    __edges_cnt: int = 0
    __nodes_cnt: int = 0
    __edges_to_resolve: list[tuple[int, int, dict]] = []  # (from_id, to_id, edge_data)
    __reference_attribute: str = "parent"

    def parse(self, data: str, reference_attribute: str, is_graph_directed: bool) -> Graph:
        self.__reset()  # so different instances won't use the same values
        self.__reference_attribute = reference_attribute # parent id
        self.__graph.directed = is_graph_directed

        json_data = json.loads(data)
        self.__build_graph(json_data, parent_id=None)
        self.__resolve_edges()

        return self.__graph

    def __reset(self):
        self.__graph = Graph()
        self.__nodes = {}
        self.__edges_cnt = 0
        self.__nodes_cnt = 0
        self.__edges_to_resolve = []

    def __build_graph(self, json_data, parent_id=None):
        if not isinstance(json_data, dict):
            return

        # if no @id => generate value
        root_node_id = self.__nodes_cnt
        self.__nodes_cnt += 1

        node_data = {}
        for key, val in json_data.items():
            if isinstance(val, (dict, list)):
                continue
            # collect node attributes
            if key not in [self.__reference_attribute, "edge_data"]:
                node_data[key] = self.__convert_value(val)

        if root_node_id not in self.__nodes:
            node = Node(root_node_id, node_data)
            self.__nodes[root_node_id] = node
            self.__graph.nodes.append(node)
        else:
            self.__nodes[root_node_id].data.update(node_data)

        current_node = self.__nodes[root_node_id]

        # add `parent -> current` edge if it exists
        if parent_id is not None and parent_id in self.__nodes:
            edge_data = {k: self.__convert_value(v) for k, v in json_data.get("edge_data", {}).items()}
            self.__add_edge(self.__nodes[parent_id], current_node, edge_data)

        if self.__reference_attribute in json_data:
            edge_data = {k: self.__convert_value(v) for k, v in json_data.get("edge_data", {}).items()}
            try:
                to_node_id = int(json_data[self.__reference_attribute])
            except ValueError:
                raise ValueError(f"Parent reference needs to be an integer id")
            self.__edges_to_resolve.append((root_node_id, to_node_id, edge_data))

        # go through children
        for key, val in json_data.items():
            if key == "edge_data":
                continue

            if isinstance(val, dict):
                self.__build_graph(val, parent_id=root_node_id)
            elif isinstance(val, list):
                for item in val:
                    self.__build_graph(item, parent_id=root_node_id)

    """
    Add an edge depending on graph type (directed/undirected).
    """
    def __add_edge(self, from_node: Node, to_node: Node, edge_data: dict | None = None):
        edge_attrs = {k: self.__convert_value(v) for k, v in (edge_data or {}).items()}

        if self.__graph.directed:
            if not self.__edge_exists(from_node, to_node):
                self.__graph.edges.append(Edge(id=self.__edges_cnt, from_node=from_node, to_node=to_node, data=edge_attrs))
                self.__edges_cnt += 1
        else:
            if not self.__edge_exists(from_node, to_node):
                self.__graph.edges.append(Edge(id=self.__edges_cnt, from_node=from_node, to_node=to_node, data=edge_attrs))
                self.__edges_cnt += 1
            if not self.__edge_exists(to_node, from_node):
                self.__graph.edges.append(Edge(id=self.__edges_cnt, from_node=from_node, to_node=to_node, data=edge_attrs))
                self.__edges_cnt += 1

    def __edge_exists(self, a: Node, b: Node) -> bool:
        return any(e.from_node == a and e.to_node == b for e in self.__graph.edges)

    """
    Resolve parent/child edges after building the graph.
    """
    def __resolve_edges(self):
        for src_id, target_id, edge_data in self.__edges_to_resolve:
            if src_id in self.__nodes and target_id in self.__nodes:
                self.__add_edge(self.__nodes[src_id], self.__nodes[target_id], edge_data)

    @staticmethod
    def __convert_value(value):
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
