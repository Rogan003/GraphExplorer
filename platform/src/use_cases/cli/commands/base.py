class Command:
    """
    Base class for all CLI commands.

    Each command operates on a workspace and receives parsed arguments
    from the CLI parser. Commands can define required or optional
    arguments and properties, and may also use positional arguments.

    Attributes:
        args (dict): Named arguments for the command, including optional "properties".
        workspace: The active workspace object on which the command operates.
        positional (list[str]): Positional arguments provided in the command.
    """
    def __init__(self, args, workspace, positional=None):
        """
        Initialize a command with arguments and a workspace.

        Args:
            args (dict): Named arguments for the command.
            workspace: The active workspace object.
            positional (list[str], optional): List of positional arguments. Defaults to empty list.
        """
        self.args = args
        self.workspace = workspace
        self.positional = positional or []

    def get_arg(self, key, default=None, required=False):
        """
        Retrieve a named argument from `args`.

        Args:
            key (str): The name of the argument to retrieve.
            default (any, optional): Default value if the argument is not present. Defaults to None.
            required (bool, optional): If True, raises ValueError when the argument is missing. Defaults to False.

        Returns:
            any: The value of the argument if present, otherwise the default.

        Raises:
            ValueError: If `required` is True and the argument is missing.
        """
        if key in self.args:
            return self.args[key]
        if required:
            raise ValueError(f"Argument '{key}' is required for {self.__class__.__name__}")
        return default

    def get_property(self, key, default=None, required=False):
        """
        Retrieve a property from the special "properties" dictionary in `args`.

        Args:
            key (str): The property name to retrieve.
            default (any, optional): Default value if the property is not present. Defaults to None.
            required (bool, optional): If True, raises ValueError when the property is missing. Defaults to False.

        Returns:
            any: The value of the property if present, otherwise the default.

        Raises:
            ValueError: If `required` is True and the property is missing.
        """
        props = self.args.get("properties", {})
        if key in props:
            return props[key]
        if required:
            raise ValueError(f"Property '{key}' is required for {self.__class__.__name__}")
        return default

    def execute(self):
        """
        Execute the command.

        This method must be implemented by each concrete command subclass.
        It defines the behavior of the command when called.

        Raises:
            NotImplementedError: Always, since subclasses must override this method.
        """
        raise NotImplementedError("Each command must implement execute()")
