from use_cases.cli.commands.base import Command
from use_cases.filter.filter_error import FilterError
from use_cases.filter.filter import Filter

class FilterGraphCommand(Command):
    """
    Command to filter nodes in a workspace graph.

    This command uses a required named argument "query" for filtering nodes,
    provided via the CLI parser.
    """

    def execute(self):

        """
        Execute the filter on a graph.

        Named arguments:
            args["query"] (str): The filter expression in format `Attribute>Value`, `Attribute<=Value`, etc. Required.

         Returns:
            str: Success message indicating the matching nodes and their properties.

        Raises:
            ValueError: If the required "query" argument is missing.
            ValueError: If no nodes matching the filter are found.
            FilterError: If the filter expression or comparator is invalid.

        Example:
            >>> parsed_command = parse_command("filter graph --query=Age>30")
            >>> cmd = FilterGraphCommand(parsed_command["args"], workspace)
            >>> cmd.execute()
            "Found nodes: [2, 5] with properties: [{'Age': 35, 'Name': 'Tom'}, {'Age': 42, 'Name': 'Alice'}]"
        """
        query = self.get_arg("query", required=True).strip()

        comparators = [">=", "<=", "!=", ">", "<", "="]
        comparator = None
        for comp in comparators:
          if comp in query:
              comparator = comp
              break

        if not comparator:
          raise ValueError(f"Invalid filter query: {query}. Must contain one of {comparators}")

        attribute_name, attribute_value = query.split(comparator, 1)
        attribute_name = attribute_name.strip()
        attribute_value = attribute_value.strip()

        if comparator == "=":
          comparator = "=="

        filters = Filter(
            attribute_name,
            comparator,
            attribute_value,
            ""
        )

        try:
            self.workspace.add_filter(filters)
            return "Filter applied successfully."

        except FilterError as fe:
            return str(fe)
