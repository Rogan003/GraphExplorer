from abc import ABC, abstractmethod
import requests

class XmlLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        pass

class XmlFileLoader(XmlLoader):
    # path here should be a file path
    def load(self, path: str) -> str:
        with open(path, "r") as file:
            return file.read()

class XmlLinkLoader(XmlLoader):
    # path here should be a link
    def load(self, path: str) -> str:
        response = requests.get(path, timeout=10)
        response.raise_for_status()
        return response.text