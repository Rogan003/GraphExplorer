from use_cases.cli.commands.base import Command
from graph_explorer_api.model.node import Node

class CreateNodeCommand(Command):
    def execute(self):
        node_id = self.args.get("--id")
        properties = self.args.get("properties", {})

        if not node_id:
            return "Error: ID is required"

        node = Node(id=node_id, data=properties)
        self.workspace.graph.add_node(node)
        return f"Node {node_id} created with {properties}"
