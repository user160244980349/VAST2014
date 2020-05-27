import csv

from tools import database, fsys
from tools.text import remove_quotes, normalize_date


def files(cfiles):
    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `all_files`")
    database.execute("PRAGMA foreign_keys = ON;")

    columns = ['name', 'path', 'content']
    query = "CREATE TABLE `all_files` (`id` integer PRIMARY KEY AUTOINCREMENT,{})".format(
        ','.join(["`%s` text" % column.lower() for column in columns]))
    database.execute(query)

    rows = []
    for file in cfiles:
        f = open(file, "r", encoding='latin1')
        rows.append('(' + ','.join([
            "\"%s\"" % value for value in [fsys.name(file), file, remove_quotes(f.read())]
        ]) + ')')

    query = "INSERT INTO `all_files` ({}) VALUES {}".format(
        ','.join(["`%s`" % column.lower() for column in columns]),
        ','.join(rows))

    database.execute(query)


def csvs(cfiles):
    for file in cfiles:

        if fsys.ext(file) == 'csv':
            table = "file_" + fsys.normalized_name(file)

            database.execute("PRAGMA foreign_keys = OFF;")
            database.execute("DROP TABLE IF EXISTS `%s`" % table)
            database.execute("PRAGMA foreign_keys = ON;")

            with open(file, 'r', encoding='latin1') as f:
                reader = csv.reader(f, delimiter=',')
                columns = next(reader)

                query = ("CREATE TABLE `%s` (`id` integer PRIMARY KEY AUTOINCREMENT,{})" % table).format(
                    ','.join(["`%s` text" % column.lower() for column in columns]))

                database.execute(query)

                rows = []
                for values in reader:
                    rows.append('(' + ','.join([
                        "'%s'" % remove_quotes(normalize_date(value)) for value in values]) + ')')

                query = ("INSERT INTO `%s` ({}) VALUES {}" % table).format(
                    ','.join(["`%s`" % column for column in columns]),
                    ','.join(rows))

                database.execute(query)
