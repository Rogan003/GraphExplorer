from data_source_xml.data_source_parser import DataSourceXmlParser
from graph_explorer_api.plugins.data_source_loaders import DataSourceFileLoader

if __name__ == "__main__":
    parser = DataSourceXmlParser()
    parser.configure_plugin(
            reference_attribute = "reference",
            loader = DataSourceFileLoader(),
            is_graph_directed = True
        )
    graph = parser.load(path="test_files/test.xml")
    print(graph)