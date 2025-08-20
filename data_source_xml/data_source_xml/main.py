from data_source_xml.data_source_xml.loader import XmlFileLoader, XmlLinkLoader
from data_source_xml.data_source_xml.parser import DataSourceXmlParser

if __name__ == "__main__":
    parser = DataSourceXmlParser()
    graph = parser.load()
    print(graph)