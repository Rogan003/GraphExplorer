from use_cases.cli.commands.edges.create_edge import CreateEdgeCommand
from use_cases.cli.commands.nodes.create_node import CreateNodeCommand
from use_cases.cli.commands.nodes.edit_node import EditNodeCommand
from use_cases.cli.commands.nodes.delete_node import DeleteNodeCommand
from use_cases.cli.commands.edges.delete_edge import DeleteEdgeCommand
from use_cases.cli.commands.edges.edit_edge import EditEdgeCommand

COMMANDS = {
    ("create", "node"): CreateNodeCommand,
    ("edit", "node"): EditNodeCommand,
    ("delete", "node"): DeleteNodeCommand,
    ("create", "edge"): CreateEdgeCommand,
    ("edit", "edge"): EditEdgeCommand,
    ("delete", "edge"): DeleteEdgeCommand,
    # TODO: add other commands here
}

def get_command_class(action, obj):
    """
    Retrieve the command class for a given CLI action and object type.

    Args:
        action (str): The action part of the command (e.g., "create").
        obj (str): The object type part of the command (e.g., "node", "edge").

    Returns:
        Command subclass | None: The corresponding command class if found,
        or None if the combination of action and object is not registered.

    Example:
        >>> get_command_class("create", "node")
        <class 'use_cases.cli.commands.create_node.CreateNodeCommand'>

        >>> get_command_class("create", "edge")
        <class 'use_cases.cli.commands.create_edge.CreateEdgeCommand'>
    """
    return COMMANDS.get((action, obj))
