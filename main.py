from files.factory import Factory
from resource import Resource


def main():

    print("hi")

    resource = Resource()
    files = []
    resource.all_paths(files)
    file_factory = Factory()

    files = file_factory.new_files(files)

    for file in files:
        file.reader_ref.read_line()


if __name__ == '__main__':
    main()
