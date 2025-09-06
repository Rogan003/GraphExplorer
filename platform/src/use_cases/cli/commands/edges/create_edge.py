from use_cases.cli.commands.base import Command
from graph_explorer_api.model.edge import Edge

class CreateEdgeCommand(Command):
    """
    Command to create an edge in a workspace graph.

    This command uses:
      - required named argument "id" for the edge ID
      - required positional arguments for source and target node IDs
      - optional properties provided via the CLI parser
    """

    def execute(self):
        """
        Execute the creation of an edge between two nodes.

        Named arguments:
            args["id"] (str): The unique identifier for the edge. Required.
            args["properties"] (dict, optional): Edge properties provided via `--property key=value`.

        Positional arguments:
            self.positional[0] (str): Source node ID.
            self.positional[1] (str): Target node ID.

        Returns:
            str: Success message if the edge is created, otherwise an error message

        Example:
            >>> parsed_command = parse_command("create edge --id=1 --property Name=Siblings 10 20")
            >>> cmd = CreateEdgeCommand(parsed_command["args"], workspace, positional=parsed_command["positional"])
            >>> cmd.execute()
            "Edge created between 10 and 20 with {'Name': 'Siblings'}"
        """
        edge_id = self.get_arg("id", required=True)
        properties = self.args.get("properties", {})

        if len(self.positional) < 2:
            return "Error: Need source and target node IDs"

        try:
          source_id = int(self.positional[0])
          target_id = int(self.positional[1])
        except IndexError:
            return "You must provide both source_id and target_id."
        except ValueError:
            return "Source ID and Target ID must be valid integers."

        source_node = next((n for n in self.workspace.graph.nodes if n.id == source_id), None)
        target_node = next((n for n in self.workspace.graph.nodes if n.id == target_id), None)

        if not source_node or not target_node:
            return f"Error: Node(s) not found: {source_id}, {target_id}"

        edge = Edge(id=edge_id, from_node=source_node, to_node=target_node, data=properties)
        self.workspace.graph.add_edge(edge)

        return f"Edge {edge_id} created between {source_id} and {target_id} with {properties}"
