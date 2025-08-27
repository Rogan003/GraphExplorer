import json

from django.template.loader import get_template
from graph_explorer_api.model.graph import Graph
from graph_explorer_api.model.node import Node

class TreeNode:
    def __init__(self, node: Node, parent: Node = None):
        self.node = node
        self.children = []
        self.parent = parent

class TreeViewService(object):
    def __init__(self):
        self.__tree_root = None
        self.__graph = None
        self.__visited = set()

    def generate_template(self, graph: Graph) -> str:
        if graph is not None and len(graph.nodes) > 0:
            self.__tree_root = TreeNode(graph.nodes[0])
            self.__graph = graph
            self.__generate_tree(self.__tree_root)
            self.__visited = set()

        json_data = self.__generate_tree_json(self.__tree_root)
        template_path = "tree_view.html"
        template = get_template(template_path)
        json_data_str = json.dumps(json_data)

        return template.render({'tree_view': json_data_str})

    def __generate_tree(self, current_node: TreeNode):
        if current_node is None:
            return None

        self.__visited.add(current_node.node.id)
        for edge in self.__graph.edges:
            if edge.from_node.id == current_node.node.id:
                child_node = TreeNode(edge.to_node, current_node)
                current_node.children.append(child_node)
                if child_node.node.id not in self.__visited:
                    self.__generate_tree(child_node)

            elif not self.__graph.directed and edge.to_node.id == current_node.node.id:
                child_node = TreeNode(edge.from_node, current_node)
                current_node.children.append(child_node)
                if child_node.node.id not in self.__visited:
                    self.__generate_tree(child_node)

    def __generate_tree_json(self, tree_node: TreeNode) -> dict:
        if tree_node is None:
            return {}

        return {
            "id": tree_node.node.id,
            **tree_node.node.data,
            "children" : [
                self.__generate_tree_json(child) for child in tree_node.children if child is not None
            ]
        }

    def empty_tree(self) -> str:
        self.__tree_root = None
        self.__graph = None
        self.__visited = set()

        template_path = "tree_view.html"
        template = get_template(template_path)
        json_data_str = json.dumps({})
        return template.render({'tree_view': json_data_str})