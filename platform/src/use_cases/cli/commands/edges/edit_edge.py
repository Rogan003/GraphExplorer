from use_cases.cli.commands.base import Command
from graph_explorer_api.model.edge import Edge

class EditEdgeCommand(Command):
    
    """
    Command to edit an edge in a workspace graph.

    This command uses a required named argument "id" for the edge ID,
    and properties provided via the CLI parser.

    """

    """
      Execute the editing of an edge.

      Named arguments:
          args["id"] (str): The unique identifier for the edge. Required.
          args["properties"] (dict): Edge properties provided via `--property key=value`.

      Returns:
          str: Success message indicating the edge ID and properties.

      Raises:
          ValueError: If the required "id" and/or "properties" argument is missing.
          ValueError: If an edge with the given "id" does not exist.
          ValueError: If an edge id is not an integer.

      Example:
          >>> parsed_command = parse_command("edit edge --id=5 --property weight=10 --property label='A-B'")
          >>> cmd = EditEdgeCommand(parsed_command["args"], workspace)
          >>> cmd.execute()
          "Edge 5 successfully edited with properties: {'weight': 10, 'label': 'A-B'}"
    """

    def execute(self):
        edge_id_arg = self.get_arg("id", required=True)
        properties = self.get_arg("properties", required=True)

        try:
            edge_id = int(edge_id_arg)
            edge = self.workspace.graph.get_edge(edge_id)
        except ValueError as e:
            if "invalid literal" in str(e):
                return f"Invalid edge ID: '{edge_id_arg}' (must be an integer)"
            return f"Error while attempting to edit: {str(e)}"

        self.workspace.graph.edit_edge(edge, properties)

        return f"Edge '{edge_id}' successfully edited. Current properties: {edge.to_dict()['data']}"
