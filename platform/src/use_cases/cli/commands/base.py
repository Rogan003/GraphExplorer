class Command:
    def __init__(self, args, positional, workspace):
        self.args = args
        self.positional = positional
        self.workspace = workspace

    def execute(self):
        raise NotImplementedError("Each command must implement execute()")