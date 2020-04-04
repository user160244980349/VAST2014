from Readers.IReader import IReader


class TxtReader(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TxtReader, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading TEXT")
        return

