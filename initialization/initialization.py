import os

import config
from initialization import convert, upload
from tools import fsys


def initialization():
    fsys.cleanup()
    fs = fsys.files(config.input_files)
    converted_fs = []

    for file in fs:
        ext = fsys.ext(file)

        if ext == 'docx':
            destination = os.path.join(config.converted_files, fsys.name(file) + '.txt')
            convert.docx2txt(file, destination)
            converted_fs.append(destination)

        if ext == 'xlsx':
            destination = os.path.join(config.converted_files, fsys.name(file) + '.csv')
            convert.xls2csv(file, destination)
            converted_fs.append(destination)

        if ext == 'txt' or ext == 'csv':
            destination = os.path.join(config.converted_files, fsys.name(file) + '.' + fsys.ext(file))
            fsys.copy(file, destination)
            converted_fs.append(destination)

    upload.files(converted_fs)
    upload.csvs(converted_fs)
