class Filter:
    def __init__(self, attribute_name=None, comparator=None, attribute_value=None, search_value=None):
        self.attribute_name = attribute_name
        self.comparator = comparator
        self.attribute_value = attribute_value
        self.search_value = search_value

    def to_dict(self):
        return {
            "attribute_name": self.attribute_name,
            "comparator": self.comparator,
            "attribute_value": self.attribute_value,
            "search_value": self.search_value,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            attribute_name=data.get("attribute_name"),
            comparator=data.get("comparator"),
            attribute_value=data.get("attribute_value"),
            search_value=data.get("search_value"),
        )