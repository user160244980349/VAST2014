from Readers.IReader import IReader


class DocxReader(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DocxReader, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading DOCX")
        return

