from enum import Enum
import json
import os

class XMLLoaderType(Enum):
    FILE = "file"
    LINK = "link"

class GraphType(Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"

class Configuration:
    CONFIG_FILE_PATH = "../config/data_source_xml_parser_config.json"

    def __init__(self):
        self.__loader_type = XMLLoaderType.FILE
        self.__reference_attribute = "reference"
        self.__graph_type = GraphType.DIRECTED
        self.__load_config()

    def get_loader_type(self) -> XMLLoaderType:
        return self.__loader_type

    def set_loader_type(self, loader_type: XMLLoaderType):
        self.__loader_type = loader_type
        self.__save_config()

    def get_reference_attribute(self) -> str:
        return self.__reference_attribute

    def set_reference_attribute(self, reference_attribute: str):
        self.__reference_attribute = reference_attribute
        self.__save_config()

    def get_graph_type(self) -> GraphType:
        return self.__graph_type

    def set_graph_type(self, graph_type: GraphType):
        self.__graph_type = graph_type
        self.__save_config()

    def __load_config(self):
        try:
            if not os.path.exists(self.CONFIG_FILE_PATH):
                return

            with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                config_data = json.load(config_file)
                self.__loader_type = XMLLoaderType(
                    config_data.get('loader_type', XMLLoaderType.FILE.value)
                )
                self.__reference_attribute = config_data.get('reference_attribute', 'reference')
                self.__graph_type = GraphType(
                    config_data.get('graph_type', GraphType.DIRECTED.value)
                )
        except (json.JSONDecodeError, FileNotFoundError, ValueError):
            return

    def __save_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE_PATH), exist_ok=True)
        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            json.dump({
                'loader_type': self.__loader_type.value,
                'reference_attribute': self.__reference_attribute,
                'graph_type': self.__graph_type.value
            }, config_file)
