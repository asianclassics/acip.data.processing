import xml.etree.ElementTree as XML


class BXml:
    def __init__(self, xml, leaf=None):
        if leaf is None:
            self.leaf = 'work'
        else:
            self.leaf = leaf

        self.doc_path = xml
        self.document = self.load_document()
        self.root = self.get_root()

    def load_document(self):
        return XML.parse(self.doc_path)

    def get_root(self):
        return self.document.getroot()

    def get_listing(self):
        new_listing = []
        for work in self.root.findall(self.leaf):
            new_listing.append(work.text)

        return new_listing
