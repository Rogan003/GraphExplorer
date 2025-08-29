from use_cases.cli.commands.create_edge import CreateEdgeCommand
from use_cases.cli.commands.create_node import CreateNodeCommand

COMMANDS = {
    ("create", "node"): CreateNodeCommand,
    ("create", "edge"): CreateEdgeCommand,
    # TODO: add other commands here
}

def get_command_class(action, obj):
    return COMMANDS.get((action, obj))