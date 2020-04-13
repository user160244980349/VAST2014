import os

import config
from tools import fsys
from initialization import convert, upload


def initialization():

    fs = fsys.files(config.resources)
    converted_fs = []

    for file in fs:
        ext = fsys.ext(file)

        if ext == 'docx':
            destination = os.path.join(fsys.directory(file), fsys.name(file) + '.txt')
            convert.docx2txt(file, destination)
            converted_fs.append(destination)

        if ext == 'xlsx':
            destination = os.path.join(fsys.directory(file), fsys.name(file) + '.csv')
            convert.xls2csv(file, destination)
            converted_fs.append(destination)

        if ext == 'txt' or ext == 'csv':
            converted_fs.append(file)

    upload.files(converted_fs)
    upload.csvs(converted_fs)
