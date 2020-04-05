from readers.ireader import IReader


class Csv(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Csv, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading CSV")
        return

