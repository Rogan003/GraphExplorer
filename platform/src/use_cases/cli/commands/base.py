class Command:
    def __init__(self, args, workspace, positional=None):
        self.args = args
        self.workspace = workspace
        self.positional = positional or []

    def get_arg(self, key, default=None, required=False):
        if key in self.args:
            return self.args[key]
        if required:
            raise ValueError(f"Argument '{key}' is required for {self.__class__.__name__}")
        return default

    def get_property(self, key, default=None, required=False):
        props = self.args.get("properties", {})
        if key in props:
            return props[key]
        if required:
            raise ValueError(f"Property '{key}' is required for {self.__class__.__name__}")
        return default

    def execute(self):
        raise NotImplementedError("Each command must implement execute()")
