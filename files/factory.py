import re
from importlib import import_module
from files.file import File
from config import readers


class Factory:

    def new_file(self, path):

        ext = re.match(r'^.*\.(\w+)$', path).group(1)

        module = import_module(readers['module'] + "." + readers[ext])
        reader = getattr(module, readers[ext].capitalize())

        file = File()
        file.ext = ext
        file.path = path
        file.reader_ref = reader()

        return file

    def new_files(self, paths):
        files = []

        for path in paths:
            file = self.new_file(path)
            files.append(file)

        return files
