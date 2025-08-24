from data_source_parser import DataSourceJSONParser

if __name__ == "__main__":
    parser = DataSourceJSONParser()
    graph = parser.load(path="test_files/test.json", )
    print(graph)