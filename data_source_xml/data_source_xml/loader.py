from abc import abstractmethod

class DataSourceXmlLoader:
    @abstractmethod
    def load(self, **kwargs) -> str:
        pass

class DataSourceXmlFileLoader(DataSourceXmlLoader):
    def load(self, file_path: str, **kwargs) -> str:
        with open(file_path, "r") as file:
            return file.read()

class DataSourceXmlLinkLoader(DataSourceXmlLoader):
    def load(self, link: str, **kwargs) -> str:
        import requests
        return requests.get(link).text