from data_source_xml.data_source_parser import DataSourceXmlParser

if __name__ == "__main__":
    parser = DataSourceXmlParser()
    graph = parser.load(path="test_files/test.xml")
    print(graph)