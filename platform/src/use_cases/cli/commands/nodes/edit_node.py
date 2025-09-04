from use_cases.cli.commands.base import Command
from graph_explorer_api.model.node import Node

class EditNodeCommand(Command):

  """
  Command to edit a node in a workspace graph.

  This command uses a required named argument "id" for the node ID,
  and properties provided via the CLI parser.
  """

  """
      Execute the editing of a node.

      Named arguments:
          args["id"] (str): The unique identifier for the node. Required.
          args["properties"] (dict): Node properties provided via `--property key=value`.

      Returns:
          str: Success message indicating the node ID and properties.

      Raises:
          ValueError: If the required "id" and/or "properties" argument is missing.
          ValueError: If a node with the given "node_id" does not exist.

      Example:
          >>> parsed_command = parse_command("edit node --id=2 --property Age=40 --property Decription="test test")
          >>> cmd = EditNodeCommand(parsed_command["args"], workspace)
          >>> cmd.execute()
          "Node 2 successfully edited with properties: {'Age': '40', 'Description'="test test"}"
      """
  def execute(self):
    node_id = self.get_arg("id", required=True)
    properties = self.get_arg("properties", required=True)

    try:
      node = self.workspace.graph.get_node(node_id)
    except ValueError as e:
        return f"Error while attempting to edit: {str(e)}"

    self.workspace.graph.edit_node(node, properties)

    return f"Node '{node_id}' successfully edited. Current properties: {node.to_dict()['data']}"
