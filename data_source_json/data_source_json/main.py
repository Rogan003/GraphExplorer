from data_source_json.data_source_parser import DataSourceJSONParser
from graph_explorer_api.plugins.data_source_loaders import DataSourceFileLoader

if __name__ == "__main__":
    parser = DataSourceJSONParser()
    parser.configure_plugin(
        reference_attribute="parent",
        loader=DataSourceFileLoader(),
        is_graph_directed=True
    )
    graph = parser.load(path="test_files/test.json")
    print(graph)
