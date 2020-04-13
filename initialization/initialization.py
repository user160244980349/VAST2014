import csv
import os
import config

from tools import database, fsys
from initialization import convert


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

    database.connect(config.database)

    query = "DROP TABLE IF EXISTS files"
    print("QUERY: %s" % query)
    database.execute(query)

    query = "CREATE TABLE files ({0})".format(
        ','.join(["`%s` text" % column for column in ['Name', 'Path', 'Content']]))
    print("QUERY: %s" % query)
    database.execute(query)

    for file in converted_fs:

        f = open(file, "r")
        query = "INSERT INTO files ({0}) VALUES ({1})".format(
            ','.join(["`%s`" % column for column in ['Name', 'Path', 'Content']]),
            ','.join(["\"%s\"" % value for value in [fsys.name(file), file, f.read()]]))
        print("QUERY: %s" % query)
        database.execute(query)

        if fsys.ext(file) == 'csv':
            table = fsys.normalized_name(file)
            query = "DROP TABLE IF EXISTS %s" % table
            print("QUERY: %s" % query)
            database.execute(query)

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                columns = next(reader)

                query = ("CREATE TABLE %s ({0})" % table).format(
                    ','.join(["'%s' text" % column for column in columns]))
                print("QUERY: %s" % query)
                database.execute(query)

                for values in reader:
                    query = "INSERT INTO %s ({0}) VALUES ({1})" % table
                    query = query.format(
                        ','.join(["`%s`" % column for column in columns]),
                        ','.join(["'%s'" % value for value in values]))
                    print("QUERY: %s" % query)
                    database.execute(query)

    database.disconnect()
