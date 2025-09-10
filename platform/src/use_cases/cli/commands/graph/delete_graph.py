from use_cases.cli.commands.base import Command

class DeleteGraphCommand(Command):
    """
    Command to delete a graph from a workspace.
    """

    def execute(self):
        """
        Execute the deletion of a graph.

        Returns:
            str: Success message indicating the graph has been deleted.

        Example:
            >>> parsed_command = parse_command("delete graph")
            >>> cmd = DeleteGraphCommand({}, workspace)
            >>> cmd.execute()
            "Graph has been successfully deleted."
        """
        self.workspace.delete_graph()

        return f"Graph has been successfully deleted."
