from Readers.IReader import IReader


class XlsxReader(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(XlsxReader, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading XLSX")
        return

