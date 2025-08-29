import shlex

def parse_command(command_str: str):
    tokens = shlex.split(command_str)
    if not tokens:
        return None
    
    action = tokens[0]
    obj_type = tokens[1] if len(tokens) > 1 else None
    
    args = {}
    positional = []
    properties = {}

    i = 2
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("--"):
            key = t[2:]
            if key == "property":
                if i + 1 >= len(tokens):
                    raise ValueError("Expected property after --property")
                prop_token = tokens[i + 1]
                if "=" not in prop_token:
                    raise ValueError(f"Invalid property format: {prop_token}")
                prop_key, prop_val = prop_token.split("=", 1)
                properties[prop_key] = prop_val
                i += 2
            else:
                if "=" not in t:
                    raise ValueError(f"Invalid argument format: {t}")
                arg_key, arg_val = t.split("=", 1)
                args[arg_key] = arg_val
                i += 1
        else:
            positional.append(t)
            i += 1

    if properties:
        args["properties"] = properties

    return {
        "action": action,
        "object": obj_type,
        "args": args,
        "positional": positional
    }
