from use_cases.cli.command_factory import get_command_class

def execute_command(parsed_command, workspace):
    """
    Execute a CLI command in the context of a workspace.

    This function takes a parsed command dictionary (from `parse_command`),
    looks up the corresponding Command class, instantiates it with the provided
    arguments, workspace, and positional parameters, and executes it.

    Args:
        parsed_command (dict): The parsed command dictionary with keys:
            - "action" (str): The command action, e.g., "create".
            - "object" (str): The object type, e.g., "node" or "edge".
            - "args" (dict): Named arguments, including any "properties".
            - "positional" (list[str]): Positional arguments, e.g., node IDs for edges.
        workspace: The active workspace object where the command operates.

    Returns:
        str: Result message from executing the command, or error message if:
            - The command is empty
            - The action/object combination is unknown

    Example:
        >>> parsed = parse_command("create node --id=10 --property Name=Alice")
        >>> execute_command(parsed, workspace)
        "Node 10 created with {'Name': 'Alice'}"

        >>> parsed = parse_command("create edge --id=100 --property Name=Siblings 10 20")
        >>> execute_command(parsed, workspace)
        "Edge 100 created between 10 and 20 with {'Name': 'Siblings'}"
    """
    if not parsed_command:
        return "Error: Empty command"

    action = parsed_command.get("action")
    obj = parsed_command.get("object")
    args = parsed_command.get("args", {})
    positional = parsed_command.get("positional", [])

    CommandClass = get_command_class(action, obj)
    if not CommandClass:
        return f"Error: Unknown command '{action} {obj}'"

    command_instance = CommandClass(args, workspace, positional=positional)
    return command_instance.execute()
