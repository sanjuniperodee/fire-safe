from xml.etree import ElementTree


class XmlParser:
    @classmethod
    def parse_xml(cls, xml_data):
        try:
            root = ElementTree.fromstring(xml_data)
            xml_dict = cls._xml_to_dict(root)
            return xml_dict
        except ElementTree.ParseError as e:
            raise ValueError(f"Failed to parse XML: {e}")

    @classmethod
    def _xml_to_dict(cls, element):
        xml_dict = {}
        for child in element:
            xml_dict[child.tag] = child.text
        return xml_dict
