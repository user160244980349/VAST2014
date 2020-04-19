from tools import database
from tools.text import remove_newlines, lemmatize
from tools.text import remove_spaces


def emails():
    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `emailheaders_info`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE emailheaders_info (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`email_id` integer, " \
            "`lemmatized_header` text, " \
            "FOREIGN KEY (`email_id`) REFERENCES `file_emailheaders`(`id`))"
    database.execute(query)

    query = "SELECT `id`, `content` " \
            "FROM `file_emailheaders`"
    records = database.execute(query)

    rows = []
    for record in records:
        file_id = record[0]
        file_content = record[1]

        lines = str.splitlines(file_content)

        header = remove_spaces(remove_newlines(header.lower()))

        rows.append('(' + ','.join([
            "%d" % file_id,
            "'%s'" % header,
            "'%s'" % lemmatize(header)]) + ')')

    query = "INSERT INTO emailheaders_info (`file_id`, `date`, `header`, `lemmatized_header`) VALUES {}".format(
        ','.join(rows))
    database.execute(query)
