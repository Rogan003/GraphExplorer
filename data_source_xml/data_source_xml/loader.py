from abc import abstractmethod

class XmlLoader:
    @abstractmethod
    def load(self, **kwargs) -> str:
        pass

class XmlFileLoader(XmlLoader):
    def load(self, file_path: str, **kwargs) -> str:
        with open(file_path, "r") as file:
            return file.read()

class XmlLinkLoader(XmlLoader):
    def load(self, link: str, **kwargs) -> str:
        import requests
        return requests.get(link).text