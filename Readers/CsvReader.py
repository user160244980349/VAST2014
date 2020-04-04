from Readers.IReader import IReader


class CsvReader(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CsvReader, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading CSV")
        return

