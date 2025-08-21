from enum import Enum
import json
import os

class XMLLoaderType(Enum):
    FILE = "file"
    LINK = "link"

class Configuration:
    CONFIG_FILE_PATH = "config/xml_config.json"

    def __init__(self):
        self.loader_type = XMLLoaderType.FILE
        self.reference_attribute = "reference"
        self.load_config()

    def load_config(self):
        try:
            if not os.path.exists(self.CONFIG_FILE_PATH):
                return

            with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                config_data = json.load(config_file)
                self.loader_type = XMLLoaderType(config_data.get('loader_type', XMLLoaderType.FILE.value))
                self.reference_attribute = config_data.get('reference_attribute', 'reference')
        except (json.JSONDecodeError, FileNotFoundError, ValueError):
            pass

    def save_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE_PATH), exist_ok=True)
        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            json.dump({
                'loader_type': self.loader_type.value,
                'reference_attribute': self.reference_attribute
            }, config_file)

    def set_loader_type(self, loader_type: XMLLoaderType):
        self.loader_type = loader_type
        self.save_config()

    def set_reference_attribute(self, reference_attribute: str):
        self.reference_attribute = reference_attribute
        self.save_config()

    def get_loader_type(self) -> XMLLoaderType:
        return self.loader_type

    def get_reference_attribute(self) -> str:
        return self.reference_attribute
