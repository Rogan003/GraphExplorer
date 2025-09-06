from use_cases.cli.commands.base import Command
from graph_explorer_api.model.edge import Edge

class DeleteEdgeCommand(Command):

  """
    Command to delete an edge from a workspace graph.

    This command uses a required named argument "id" for the edge ID.
    It will prevent deletion if the edge does not exist.
  """

  """
  Execute the deletion of an edge.

  Named arguments:
      args["id"] (str): The unique identifier for the edge. Required.

  Returns:
      str: Success message indicating the edge ID has been deleted, or an error message if the edge does not exist.

  Raises:
      ValueError: If the required "id" argument is missing.
      ValueError: If an edge with the given "id" does not exist.
      ValueError: If argument id is not an integer.

  Example:
      >>> parsed_command = parse_command("delete edge --id=5")
      >>> cmd = DeleteEdgeCommand(parsed_command["args"], workspace)
      >>> cmd.execute()
      "Edge 5 successfully deleted."
  """
  
  def execute(self):
    edge_id_arg = self.get_arg("id", required=True)

    try:
        edge_id = int(edge_id_arg)
    except ValueError:
        return f"Invalid edge ID: '{edge_id_arg}' (must be an integer)"

    try:
        self.workspace.graph.remove_edge(edge_id)
    except ValueError as e:
        return f"Error while attempting to delete edge: {str(e)}"

    return f"Edge '{edge_id}' successfully deleted."
