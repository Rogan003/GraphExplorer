from abc import ABC, abstractmethod

import requests

class JSONLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        pass

#@Deprecated("The same method exists in `data_source_xml/data_source_xml/loader.py` - should be generic for JSON and XML")
class JSONFileLoader(JSONLoader):
    def load(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()

#@Deprecated("The same method exists in `data_source_xml/data_source_xml/loader.py` - should be generic for JSON and XML")
class JSONUrlLoader(JSONLoader):
    def load(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text