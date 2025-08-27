import pkg_resources
from graph_explorer_api.plugins.data_source_loaders import DataSourceLoader
from use_cases.const import DATA_SOURCE_LOADERS_GROUP

def find_loader(id: str) -> DataSourceLoader:
    loaders_names = pkg_resources.iter_entry_points(group=DATA_SOURCE_LOADERS_GROUP)

    for loader_name in loaders_names:
        loader = loader_name.load()()
        if loader.identifier() == id or str(loader_name.name) == id:
            return loader