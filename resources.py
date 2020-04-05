from config import resources
from os import walk


class Resources:

    def root(self):
        return resources['root']

    def path(self, postfix):
        return resources['root'] + "\\" + resources[postfix]

    def file_paths(self, postfix, files):
        for (dir_path, dir_names, file_names) in walk(self.path(postfix)):
            files.extend([dir_path + "\\" + file_name for file_name in file_names])
        return

    def all_paths(self, files):
        for postfix in resources:
            if postfix == 'root':
                continue
            self.file_paths(postfix, files)
        return
