from config import resources
from config import postfixes
from os import walk


class Resource:

    def __init__(self):
        self._root = resources
        self._postfixes = postfixes

    def root(self):
        return self._root

    def path(self, postfix):
        return self._root + "\\" + self._postfixes[postfix]

    def file_paths(self, postfix, files):
        for (dir_path, dir_names, file_names) in walk(self.path(postfix)):
            files.extend([dir_path + "\\" + file_name for file_name in file_names])
        return

    def all_paths(self, files):
        for postfix in self._postfixes:
            self.file_paths(postfix, files)
        return
