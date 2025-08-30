from use_cases.cli.commands.base import Command
from graph_explorer_api.model.edge import Edge

class CreateEdgeCommand(Command):
    """
    Command to create an edge between two nodes in a workspace graph.

    This command uses positional arguments for source and target node IDs,
    and optional properties provided via the CLI parser.
    """

    def execute(self):
        """
        Execute the creation of an edge between two nodes.

        Positional arguments:
            self.positional[0] (str): Source node ID.
            self.positional[1] (str): Target node ID.

        Named arguments:
            args["properties"] (dict, optional): Edge properties provided via `--property key=value`.

        Returns:
            str: Success message if the edge is created, otherwise an error message:
                - "Error: Need source and target node IDs" if positional arguments are missing
                - "Error: Node(s) not found: source_id, target_id" if either node does not exist

        Example:
            >>> parsed_command = parse_command("create edge 10 20 --property Name=Siblings")
            >>> cmd = CreateEdgeCommand(parsed_command["args"], workspace, positional=parsed_command["positional"])
            >>> cmd.execute()
            "Edge created between 10 and 20 with {'Name': 'Siblings'}"
        """
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
