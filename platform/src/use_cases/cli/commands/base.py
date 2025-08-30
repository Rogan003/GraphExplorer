class Command:
    def __init__(self, args, workspace):
        self.args = args
        self.workspace = workspace

    def execute(self):
        raise NotImplementedError("Each command must implement execute()")