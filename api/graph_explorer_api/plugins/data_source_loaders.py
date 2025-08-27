from abc import abstractmethod, ABC

import requests

class DataSourceLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:
        pass

class DataSourceFileLoader(DataSourceLoader):
    # path in this context here should be a file path
    def load(self, path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    def identifier(self) -> str:
        return "DataSourceFileLoader"

class DataSourceUrlLoader(DataSourceLoader):
    # path in this context is a url, path on the web
    def load(self, path: str) -> str:
        response = requests.get(path, timeout=10)
        response.raise_for_status()
        return response.text

    def identifier(self) -> str:
        return "DataSourceUrlLoader"