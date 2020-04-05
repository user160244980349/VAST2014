from readers.ireader import IReader


class Txt(IReader):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Txt, cls).__new__(cls)
        return cls.instance

    def read_line(self):
        print("reading TEXT")
        return

