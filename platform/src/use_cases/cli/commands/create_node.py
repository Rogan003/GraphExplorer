from use_cases.cli.commands.base import Command
from graph_explorer_api.model.node import Node

class CreateNodeCommand(Command):
    """
    Command to create a node in a workspace graph.

    This command uses a required named argument "id" for the node ID,
    and optional properties provided via the CLI parser.
    """

    def execute(self):
        """
        Execute the creation of a node.

        Named arguments:
            args["id"] (str): The unique identifier for the node. Required.
            args["properties"] (dict, optional): Node properties provided via `--property key=value`.

        Returns:
            str: Success message indicating the node ID and properties.

        Raises:
            ValueError: If the required "id" argument is missing.

        Example:
            >>> parsed_command = parse_command("create node --id=10 --property Name=Alice --property Age=25")
            >>> cmd = CreateNodeCommand(parsed_command["args"], workspace)
            >>> cmd.execute()
            "Node 10 created with {'Name': 'Alice', 'Age': '25'}"
        """
        node_id = self.get_arg("id", required=True)
        properties = self.args.get("properties", {})

        node = Node(id=node_id, data=properties)
        self.workspace.graph.add_node(node)

        return f"Node {node_id} created with {properties}"
