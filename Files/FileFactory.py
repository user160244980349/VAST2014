import re
from config import readers
from Files.File import File


class FileFactory:

    def new_file(self, path):
        file = File()

        file.ext = re.match(r'^.*\.(\w+)$', path).group(1)
        file.path = path

        module = __import__(readers[file.ext])
        reader = getattr(module, readers[file.ext])

        file.reader_ref = reader()

        return file

    def new_files(self, paths):
        files = []

        for path in paths:
            file = self.new_file(path)
            files.append(file)

        return files
