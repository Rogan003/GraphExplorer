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
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception:
            return ""

    def identifier(self) -> str:
        return "data_source_file_loader"

class DataSourceUrlLoader(DataSourceLoader):
    # path in this context is a url, path on the web
    def load(self, path: str) -> str:
        if not path or not path.startswith("http"):
            return ""

        response = requests.get(path, timeout=10)
        response.raise_for_status()
        return response.text

    def identifier(self) -> str:
        return "data_source_url_loader"