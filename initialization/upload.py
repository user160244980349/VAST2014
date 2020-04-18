import csv
from dateutil.parser import parse

import config
from tools import database, fsys
from tools.text import remove_quotes


def files(cfiles):

    database.connect(config.database)

    query = "DROP TABLE IF EXISTS all_files"
    database.execute(query)

    columns = ['name', 'path', 'content']
    query = "CREATE TABLE all_files (`id` integer PRIMARY KEY AUTOINCREMENT,{})".format(
        ','.join(["`%s` text" % column.lower() for column in columns]))
    database.execute(query)

    rows = []
    for file in cfiles:
        f = open(file, "r")
        rows.append('(' + ','.join([
            "\"%s\"" % value for value in [fsys.name(file), file, remove_quotes(f.read())]
        ]) + ')')

    query = "INSERT INTO all_files ({}) VALUES {}".format(
        ','.join(["`%s`" % column.lower() for column in columns]),
        ','.join(rows))

    database.execute(query)
    database.disconnect()


def csvs(cfiles):

    database.connect(config.database)

    for file in cfiles:

        if fsys.ext(file) == 'csv':
            table = "file_" + fsys.normalized_name(file)
            query = "DROP TABLE IF EXISTS %s" % table
            database.execute(query)

            with open(file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                columns = next(reader)

                query = ("CREATE TABLE %s (`id` integer PRIMARY KEY AUTOINCREMENT,{})" % table).format(
                    ','.join(["`%s` text" % column.lower() for column in columns]))

                database.execute(query)

                rows = []
                for values in reader:
                    rows.append('(' + ','.join(["'%s'" % remove_quotes(value) for value in normalize_dates(values)]) + ')')

                query = ("INSERT INTO %s ({}) VALUES {}" % table).format(
                    ','.join(["`%s`" % column for column in columns]),
                    ','.join(rows))

                database.execute(query)

    database.disconnect()


def normalize_dates(values):

    for i in range(len(values)):
        if is_date(values[i]):
            values[i] = parse(values[i]).strftime("%d-%m-%y %H:%M:%S")

    return values


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
