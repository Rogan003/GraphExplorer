from use_cases.cli.commands.base import Command
from graph_explorer_api.model.node import Node

class CreateNodeCommand(Command):
    def execute(self):
        node_id = self.get_arg("id", required=True)
        properties = self.args.get("properties", {})

        node = Node(id=node_id, data=properties)
        self.workspace.graph.add_node(node)

        return f"Node {node_id} created with {properties}"
