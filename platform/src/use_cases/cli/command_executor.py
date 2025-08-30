from use_cases.cli.command_factory import get_command_class

def execute_command(parsed_command, workspace):
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
