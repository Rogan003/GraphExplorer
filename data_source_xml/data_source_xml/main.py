from data_source_xml.data_source_xml.loader import XmlFileLoader, XmlLinkLoader

if __name__ == "__main__":
    loader = XmlFileLoader()
    xml = loader.load("../test_files/test.xml")
    print(xml)
    loader2 = XmlLinkLoader()
    xml2 = loader2.load("https://www.reddit.com")
    print(xml2)