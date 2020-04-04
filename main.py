from Files.FileFactory import FileFactory
from Files.Resource import Resource


def main():

    resources = Resource()
    files = []
    resources.get_all_file_paths(files)
    file_factory = FileFactory()

    files = file_factory.new_files(files)

    for file in files:
        file.reader_ref.read_line()


if __name__ == '__main__':
    main()
