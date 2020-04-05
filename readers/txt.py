from readers.ireader import IReader


class Txt(IReader):

    def __init__(self):
        self._file = None
        return

    def open(self, path):
        self._file = open(path, "r")

    def close(self):
        self._file.close()

    def read(self):
        print("reading TEXT")
        return self._file.read()

