from use_cases.cli.commands.base import Command
from use_cases.filter.filter_error import FilterError
from use_cases.filter.filter import Filter

class SearchGraphCommand(Command):
    """
    Command to search nodes in a workspace graph.

    This command uses a required named argument "query" for searching nodes,
    provided via the CLI parser.
    """

    def execute(self):
        """
        Execute the search on a graph.

        Named arguments:
            args["query"] (str): The search value to look for in node properties. Required.

        Returns:
            str: Success message indicating the matching nodes and their properties.

        Raises:
            ValueError: If the required "query" argument is missing.
            ValueError: If no nodes matching the query are found.

        Example:
            >>> parsed_command = parse_command("search graph --query=Tom")
            >>> cmd = SearchGraphCommand(parsed_command["args"], workspace)
            >>> cmd.execute()
          "Found nodes: [2] with properties: {'Name': 'Tom', 'Age': '40'}"
        """
        search_value = self.get_arg("query", required=True).strip()

        filters = Filter(
            "",
            "",
            "",
            search_value
        )

        try:
            self.workspace.add_filter(filters)
            return "Filter applied successfully."

        except FilterError as fe:
            return str(fe)