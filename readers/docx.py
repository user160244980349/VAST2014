from readers.ireader import IReader


class Docx(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Docx, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading DOCX")
        return

