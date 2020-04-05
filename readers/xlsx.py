from readers.ireader import IReader


class Xlsx(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Xlsx, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading XLSX")
        return

