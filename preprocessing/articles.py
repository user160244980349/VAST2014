from tools import database
from tools.text import is_date, remove_newlines, normalize_date, lemmatize, remove_specchars
from tools.text import remove_spaces


def articles():
    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `articles_info`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE `articles_info` (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`file_id` integer, " \
            "`date` text, " \
            "`header` text, " \
            "`lemmatized_header` text, " \
            "FOREIGN KEY (`file_id`) REFERENCES `all_files`(`id`))"
    database.execute(query)

    query = "SELECT `id`, `content` " \
            "FROM `all_files` " \
            "WHERE REGEXP(`name`, '^[0-9]+$')"
    records = database.execute(query)

    rows = []
    for record in records:
        file_id = record[0]
        file_content = record[1]

        lines = str.splitlines(file_content)

        date = ''
        header = []

        for line in lines:
            if is_date(line):
                date = normalize_date(line)
                break
            else:
                header.append(line)

        header_str = remove_spaces(
            remove_newlines(
                remove_specchars(' '.join(header).lower())))

        rows.append('(' + ','.join([
            "%d" % file_id,
            "'%s'" % date,
            "'%s'" % header_str,
            "'%s'" % lemmatize(header_str)]) + ')')

    query = "INSERT INTO `articles_info` (`file_id`, `date`, `header`, `lemmatized_header`) VALUES {}".format(
        ','.join(rows))
    database.execute(query)
