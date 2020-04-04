from config import root
from config import postfixes
from os import walk


class Resource:
    def __init__(self):
        self._root = root
        self._postfixes = postfixes

    def get_root(self):
        return self._root

    def get_path(self, postfix):
        return self._root + "\\" + self._postfixes[postfix]

    def get_file_paths(self, postfix, files):
        for (dirpath, dirnames, filenames) in walk(self.get_path(postfix)):
            files.extend([dirpath + "\\" + filename for filename in filenames])
        return

    def get_all_file_paths(self, files):
        for postfix in self._postfixes:
            self.get_file_paths(postfix, files)
        return
