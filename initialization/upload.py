import csv

import config
from tools import database, fsys
from tools.text import remove_quotes


def files(cfiles):

    database.connect(config.database)

    query = "DROP TABLE IF EXISTS files"
    database.execute(query)

    query = "CREATE TABLE files ({})".format(
        ','.join(["`%s` text" % column for column in ['Name', 'Path', 'Content']]))
    database.execute(query)

    rows = []
    for file in cfiles:
        f = open(file, "r")
        rows.append('(' + ','.join([
            "\"%s\"" % value for value in [fsys.name(file), file, remove_quotes(f.read())]
        ]) + ')')

    query = "INSERT INTO files ({}) VALUES {}".format(
        ','.join(["`%s`" % column for column in ['Name', 'Path', 'Content']]),
        ','.join(rows))

    database.execute(query)
    database.disconnect()


def csvs(cfiles):

    database.connect(config.database)

    for file in cfiles:

        if fsys.ext(file) == 'csv':
            table = fsys.normalized_name(file)
            query = "DROP TABLE IF EXISTS %s" % table
            database.execute(query)

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                columns = next(reader)

                query = ("CREATE TABLE %s ({0})" % table).format(
                    ','.join(["'%s' text" % column for column in columns]))
                database.execute(query)

                rows = []
                for values in reader:
                    rows.append('(' + ','.join(["'%s'" % remove_quotes(value) for value in values]) + ')')

                query = ("INSERT INTO %s ({}) VALUES {}" % table).format(
                    ','.join(["`%s`" % column for column in columns]),
                    ','.join(rows))

                database.execute(query)

    database.disconnect()
