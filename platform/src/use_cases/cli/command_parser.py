import shlex

def _parse_property(tokens, i, properties):
    if i + 1 >= len(tokens):
        raise ValueError("Expected property after --property")
    prop_token = tokens[i + 1]
    if "=" not in prop_token:
        raise ValueError(f"Invalid property format: {prop_token}")
    key, val = prop_token.split("=", 1)
    properties[key] = val
    return i + 2

def _parse_arg(token, args):
    if "=" not in token:
        raise ValueError(f"Invalid argument format: {token}")
    key, val = token[2:].split("=", 1)
    args[key] = val


def parse_command(command_str: str):
    """
    Parses a CLI-style command string into structured components.

    Args:
        command_str (str): Command line string to parse. 
            Example: 'create node --id=1 --property Name=Alice --property Age=25'

    Returns:
        dict | None: A dictionary with the following keys, or None if the input is empty:
            - "action" (str): The command action (first token), e.g. "create".
            - "object" (str | None): The object type (second token), e.g. "node".
            - "args" (dict): Named arguments provided with `--key=value`.
                - Special key "properties" (dict) if `--property key=value` tokens were present.

    Raises:
        ValueError: If an argument or property token is malformed 
            (e.g. missing '=', or `--property` not followed by key=value).
    """
    tokens = shlex.split(command_str)
    if not tokens:
        return None

    action, obj_type, *rest = tokens
    args, properties = {}, {}

    i = 0
    while i < len(rest):
        t = rest[i]
        if t.startswith("--"):
            if t == "--property":
                i = _parse_property(rest, i, properties)
            else:
                _parse_arg(t, args)
                i += 1
        else:
            raise ValueError(f"Unexpected positional argument: {t}")

    if properties:
        args["properties"] = properties

    return {
        "action": action,
        "object": obj_type if obj_type else None,
        "args": args
    }
