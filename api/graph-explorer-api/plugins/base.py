from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base class for all plugins."""

    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the plugin.
        
        :return: The name of the plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the plugin.

        :return: The unique identifier of the plugin.
        :rtype: str
        """
        pass
