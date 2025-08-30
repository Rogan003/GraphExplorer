from use_cases.cli.commands.base import Command
from graph_explorer_api.model.edge import Edge

class CreateEdgeCommand(Command):
    def execute(self):
        properties = self.args.get("properties", {})

        if len(self.positional) < 2:
            return "Error: Need source and target node IDs"
        source_id, target_id = self.positional[0], self.positional[1]

        source_node = next((n for n in self.workspace.graph.nodes if n.id == source_id), None)
        target_node = next((n for n in self.workspace.graph.nodes if n.id == target_id), None)

        if not source_node or not target_node:
            return f"Error: Node(s) not found: {source_id}, {target_id}"

        edge = Edge(from_node=source_node, to_node=target_node)
        self.workspace.graph.add_edge(edge)

        return f"Edge created between {source_id} and {target_id} with {properties}"
