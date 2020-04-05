from files.factory import Factory
from resources import Resources


def main():

    resource = Resources()

    file_paths = []
    resource.all_paths(file_paths)

    file_factory = Factory()
    files = file_factory.new_files(file_paths)

    for file in files:
        print(file.reader_ref)


if __name__ == '__main__':
    main()
