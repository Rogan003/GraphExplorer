from use_cases.cli.command_factory import get_command_class

def execute_command(command, workspace):
    action = command["action"]
    obj = command["object"]
    args = command["args"]

    CommandClass = get_command_class(action, obj)
    if not CommandClass:
        return f"Unknown command: {action} {obj}"

    cmd_instance = CommandClass(args, workspace)
    return cmd_instance.execute()