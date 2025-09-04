from use_cases.cli.commands.base import Command
from graph_explorer_api.model.node import Node

class DeleteNodeCommand(Command):

  """
    Command to delete a node from a workspace graph.

    This command uses a required named argument "id" for the node ID.
    It will prevent deletion if the node has any connected edges.
  """

  """
    Execute the deletion of a node.

    Named arguments:
        args["id"] (str): The unique identifier for the node. Required.

    Returns:
        str: Success message indicating the node ID has been deleted, or an error message if the node has edges.

    Raises:
        ValueError: If the required "id" argument is missing.
        ValueError: If a node with the given "node_id" does not exist.

    Example:
        >>> parsed_command = parse_command("delete node --id=2")
        >>> cmd = DeleteNodeCommand(parsed_command["args"], workspace)
        >>> cmd.execute()
        "Node 2 successfully deleted."
  """
  
  def execute(self):
    node_id = self.get_arg("id", required=True)

    if self.workspace.graph.has_edges(node_id):
      return "Please remove edges before deleting the node."
    
    try:
      self.workspace.graph.remove_node(node_id)
    except ValueError as e:
      return f"Error while attempting to delete node: {str(e)}"

    return f"Node '{node_id}' successfully deleted."
